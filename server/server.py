import argparse
import sys
import time
from threading import Lock

from flask import Flask, jsonify
from flask_socketio import SocketIO, join_room, leave_room
from flask_socketio import emit

import server_logic
from PlayerAction import PlayerAction
from def_gevents import SERV_COMM_KEY


thread = None
thread_lock = Lock()


# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
# socketio = SocketIO(app)

# @app.route('/')
# def sessions():
#    return render_template('session.html')

# def messageReceived(methods=['GET', 'POST']):
#    print('message was received!!!')

# @socketio.on('my event')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#    print('received my event: ' + str(json))
#    socketio.emit('my response', json, callback=messageReceived)

# if __name__ == '__main__':
#     socketio.run(app, port=tmp['port'], host=tmp['host']) #debug=True)
#     #socketio.run(app, port=8100, host='0.0.0.0')

# - temporaire
onlyroom = None
async_mode = "gevent"

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)

_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument('-h', '--host', help='specify host', required=True)
_parser.add_argument('-p', '--port', help='specify port', required=True)

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
def move(plcode, direct):  # can use with direct==-1 to just query the position...
    #if not gs_init:
    #    gs_init = server_logic.loadstate(gamestate)
    plcode = int(plcode)
    server_logic.maj_gamestate(plcode, int(direct))
    return jsonify(server_logic.locate_player(plcode))


# @app.route('/statesig')
# def statesig():
#     #global gs_init, gamestate
#     #if not gs_init:
#     #    gs_init = server_logic.loadstate(gamestate)
#     m = hashlib.sha224()
#     clients = list(gamestate.keys())
#     clients.sort()
#     for c in clients:
#         m.update('{}{}{}'.format(c, gamestate[c][0], gamestate[c][1]).encode('ascii'))
#     return jsonify(m.hexdigest())


@app.route('/save')
def save():
    pass


# /////////////////////////////////////
#  websockets interface
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@socketio.on('push_action')
def handle_push_action(act_serial):
    player_action = PlayerAction.deserialize(act_serial)
    da_actorid = player_action.actor_id
    act_type = player_action.action_t

    room_name = server_logic.fetch_room(da_actorid)
    assert room_name is not None

    # - bombs
    if PlayerAction.T_BOMB == act_type:
        print('player {} is posing bomb!'.format(da_actorid))
        new_b_date = time.time()
        i, j = server_logic.locate_player(da_actorid)
        server_logic.bombs[(i, j)] = new_b_date

        kwargs = {'author': da_actorid, 'genesis_t': new_b_date, 'x': i, 'y': j}
        notify(room_name, 'bomb_creation', kwargs)

    # - movements
    elif PlayerAction.T_MOVEMENT == act_type:
        server_logic.maj_gamestate(da_actorid, int(player_action.direction))
        newi, newj = server_logic.locate_player(da_actorid)
        kwargs = {'plcode': da_actorid, 'new_pos': [newi, newj]}
        notify(room_name, 'player_movement', kwargs)


@socketio.on('connect')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(bomb_checking)

    kwargs = {'playercode': server_logic.gen_username()}
    notify(None, 'connection_ok', kwargs)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('join')
def on_join(data):
    # tmp
    global onlyroom

    rname = 'bomberman#{}'.format(data['room_num'])
    join_room(rname)
    server_logic.save_room(data['username'], rname)

    plcode = data['username']
    server_logic.spawn_player(plcode)

    # temporaire: for now theres only one active room tbh
    onlyroom = rname

    print('{} has entered {}'.format(plcode, rname))
    notify(rname, 'other_guy_came', {'username': plcode})


@socketio.on('leave')
def on_leave(data):
    rname = 'bomberman#{}'.format(data['room_num'])
    leave_room(rname)
    server_logic.save_room(data['username'], None)

    print('{} has left {}'.format(data['username'], rname))


# -------- multiproc ---
def bomb_checking():
    print('checking for bombs...')
    sys.stdout.flush()
    to_be_rem = list()

    while not server_logic.force_quit:
        del to_be_rem[:]
        # check for bomb explosions
        tnow = time.time()
        for bombpos, bdate in server_logic.bombs.items():
            if (tnow - bdate) < server_logic.BOMB_DELAY:
                continue
            # a bomb explodes!
            print('a bomb explodes!')

            # special way to emit... Non dependant of the active http connection
            socketio.emit(
                'server_notification',
                {SERV_COMM_KEY:'bomb_explosion', 'x': bombpos[0], 'y': bombpos[1]}
            )
            to_be_rem.append(bombpos)

        for elt in to_be_rem:
            del server_logic.bombs[elt]
        socketio.sleep(0.5)


if __name__ == '__main__':
    tmp = _parser.parse_args()
    socketio.run(app, port=int(tmp.port))
