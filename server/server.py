import argparse
import hashlib

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_socketio import emit
import server_logic
from PlayerAction import PlayerAction
from def_gevents import SERV_COMM_KEY

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


app = Flask(__name__)
socketio = SocketIO(app)

_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument('-h', '--host', help='specify host', required=True)
_parser.add_argument('-p', '--port', help='specify port', required=True)

cpt = 0
gamestate = dict()
BSUP = 8
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
    global gs_init, gamestate, BSUP
    if not gs_init:
        gs_init = server_logic.loadstate(gamestate)
    server_logic.maj_gamestate(gamestate, int(plcode), int(direct))
    return jsonify(gamestate[int(plcode)])


@app.route('/statesig')
def statesig():
    global gs_init, gamestate
    if not gs_init:
        gs_init = server_logic.loadstate(gamestate)

    m = hashlib.sha224()
    clients = list(gamestate.keys())
    clients.sort()
    for c in clients:
        m.update('{}{}{}'.format(c, gamestate[c][0], gamestate[c][1]).encode('ascii'))
    return jsonify(m.hexdigest())


@app.route('/save')
def save():
    pass


# /////////////////////////////////////
#  websockets interface
# \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
@socketio.on('push_action')
def handle_push_action(act_serial):
    global gamestate

    act_obj = PlayerAction.deserialize(act_serial)

    print('received server side {} '.format(act_obj))
    # uname = margs[0]
    # direction = margs[1]

    room_name = server_logic.fetch_room(act_obj.actor_id)
    plcode = act_obj.actor_id

    if act_obj.action_t == PlayerAction.T_MOVEMENT:
        server_logic.maj_gamestate(gamestate, plcode, int(act_obj.direction))
        for c in gamestate.keys():
            i, j = gamestate[c]
            print('emit msg')

            kwargs = {'plcode': c, 'new_pos': [i, j]}
            notify(room_name, 'player_movement', kwargs)
            emit('player_movement', kwargs, room=room_name)


@socketio.on('connect')
def test_connect():
    kwargs = {'playercode': server_logic.gen_username()}
    notify(None, 'connection_ok', kwargs)


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('join')
def on_join(data):
    global gamestate

    rname = 'bomberman#{}'.format(data['room_num'])
    join_room(rname)
    server_logic.save_room(data['username'], rname)

    plcode = data['username']
    gamestate[plcode] = [0, 1]

    print('{} has entered {}'.format(plcode, rname))
    notify(rname, 'other_guy_came', {'username': plcode})


@socketio.on('leave')
def on_leave(data):
    rname = 'bomberman#{}'.format(data['room_num'])
    leave_room(rname)
    server_logic.save_room(data['username'], None)

    print('{} has left {}'.format(data['username'], rname))


if __name__ == '__main__':
    tmp = _parser.parse_args()
    socketio.run(app, port=int(tmp.port))
