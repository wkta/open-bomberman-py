import argparse
import sys
import time
from threading import Lock

from flask import Flask, jsonify
from flask_socketio import SocketIO, join_room, leave_room
from flask_socketio import emit

import server_logic
from PlayerAction import PlayerAction
from WorldModel import WorldModel
from def_gevents import SERV_COMM_KEY


_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument('-h', '--host', help='specify host', required=True)
_parser.add_argument('-p', '--port', help='specify port', required=True)

server_gamelogic_thread = None
thread_lock = Lock()
onlyroom = None
async_mode = "gevent"
app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
cpt = 0
gs_init = False


def notify(roomname, event_name, coremon_kwargs):
    """
    generic procedure sending things to connected game clients...
    """
    # TODO test si le event_name matche effectivement un game event déclaré
    pass

    coremon_kwargs[SERV_COMM_KEY] = event_name
    if roomname:
        emit('server_notification', coremon_kwargs, room=roomname)
    else:
        emit('server_notification', coremon_kwargs)


# /////////////////////////////////////
#  classic routes
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@app.route('/')
def index():
    global cpt
    cpt += 1
    return "hello there, req #{}".format(cpt)


@app.route('/move/<plcode>/<direct>')
def move(plcode, direct):
    # user can give direct==-1 just to query the position...
    plcode = int(plcode)
    server_logic.maj_gamestate(plcode, int(direct))
    return jsonify(server_logic.world.player_location(plcode))


@app.route('/save')
def save():
    pass


# /////////////////////////////////////
#  websockets interface
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@socketio.on('connect')
def test_connect():
    global server_gamelogic_thread, socketio
    print('***reception socketio.connect***')
    with thread_lock:
        if server_gamelogic_thread is None:  # need to start only 1 gamelogic thread, no more!
            server_gamelogic_thread = socketio.start_background_task(server_side_gameloop)

    new_plcode = server_logic.gen_username()
    adhoc_gfx = server_logic.world.use_new_gfxid(new_plcode)
    kwargs = {'gamestate': server_logic.world.serialize(), 'playercode': new_plcode, 'chosengfx': adhoc_gfx}
    notify(None, 'connection_ok', kwargs)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('join')
def on_join(data):
    global onlyroom
    rname = 'bomberman#{}'.format(data['room_num'])
    join_room(rname)
    server_logic.save_room(data['username'], rname)
    plcode = data['username']
    server_logic.world.spawn_player(plcode, time.time())
    onlyroom = rname  # temp.: for now theres only one active room tbh
    print('{} has entered {}'.format(plcode, rname))
    alldatas = {
        'gamestate': server_logic.world.serialize(),
        'playercode': int(plcode),
        'chosengfx': server_logic.world.gfxs[int(plcode)]
    }
    notify(rname, 'other_guy_came', alldatas)
    print('other_guy_came')
    print(str(alldatas['chosengfx']))


@socketio.on('leave')
def on_leave(data):
    rname = 'bomberman#{}'.format(data['room_num'])
    leave_room(rname)
    server_logic.save_room(data['username'], None)
    print('{} has left {}'.format(data['username'], rname))


@socketio.on('push_action')
def handle_push_action(act_serial):
    player_action = PlayerAction.deserialize(act_serial)
    da_actorid = player_action.actor_id
    act_type = player_action.action_t
    room_name = server_logic.fetch_room(da_actorid)
    if room_name is None:
        raise ValueError('at that point room_name shouldnt be None')

    if PlayerAction.T_BOMB == act_type:  # game action: plant bomb
        with thread_lock:
            print('player {} is posing bomb!'.format(da_actorid))
            new_b_date = time.time() + WorldModel.BOMB_DELAY
            server_logic.world.drop_bomb(da_actorid, new_b_date)
            kwargs = {'gamestate': server_logic.world.serialize()}
            notify(room_name, 'bomb_creation', kwargs)

    elif PlayerAction.T_MOVEMENT == act_type:  # game action: move
        change_occurs = server_logic.maj_gamestate(da_actorid, int(player_action.direction))
        if change_occurs:
            kwargs = {'gamestate': server_logic.world.serialize()}
            notify(room_name, 'player_movement', kwargs)


def broadcast_event(e_type_camelcase) -> None:
    """
    A special way to emit... it is not dependant on the active http connection
    :param e_type_camelcase: str, the game event type
    """
    global socketio
    socketio.emit(
        'server_notification', {
            SERV_COMM_KEY: e_type_camelcase, 'gamestate': server_logic.world.serialize()
        }
    )


# -------- multiproc ---
def server_side_gameloop():
    global socketio

    print('checking for match start...')
    sys.stdout.flush()
    while not server_logic.world.has_match_started():
        tnow = time.time()
        if server_logic.world.can_start(tnow):
            print('OK match starting!')
            server_logic.world.start_match()
            broadcast_event('challenge_starts')
        else:
            socketio.sleep(1.0)

    print('checking for bombs...')
    sys.stdout.flush()
    to_be_rem = list()

    while not server_logic.force_quit:

        with thread_lock:
            tnow = time.time()
            del to_be_rem[:]

            # compte bombes a exploser
            for elt in server_logic.world.list_bombs():
                i, j, _, bdate = elt
                bombpos = (i, j)

                if tnow >= bdate:
                    # a bomb explodes!
                    print('a bomb explodes!')
                    to_be_rem.append(bombpos)

            if len(to_be_rem) > 0:
                for id_pos in to_be_rem:
                    print('removing bomb {}'.format(id_pos))
                    server_logic.world.trigger_explosion(id_pos)

                broadcast_event('bomb_explosion')

                if server_logic.world.match_winner is not None:
                    broadcast_event('challenge_ends')
            # - fin thread lock

        socketio.sleep(0.25)


if __name__ == '__main__':
    tmp = _parser.parse_args()
    print('open bomberman py SERVER')
    print('host= {} | port= {}'.format(tmp.host, tmp.port))
    socketio.run(app, host=tmp.host, port=int(tmp.port))
