import argparse
import hashlib

from flask import Flask, jsonify, request
from flask_socketio import SocketIO, join_room, leave_room
from flask_socketio import emit

import server_logic


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
@socketio.on('pushmove')
def handle_pushmove(margs):
    global gs_init, gamestate
    print('received pushmove')

    #if not gs_init:
    #    gs_init = server_logic.loadstate(gamestate)

    uname = margs[0]
    direction = margs[1]

    room_name = server_logic.fetch_room(uname)
    plcode = server_logic.user_to_code(uname)

    server_logic.maj_gamestate(gamestate, plcode, int(direction))
    for c in gamestate.keys():
        i, j = gamestate[c]
        emit('player_moved', {'code': c, 'newpos': [i, j]}, room=room_name)


# @socketio.on('move')
# def move(data):
#     emit('death', {'data': ''})


@socketio.on('connect')
def test_connect():
    print(request.sid)
    emit('connection_ok', server_logic.gen_username())
    # time.sleep(5)
    # emit('death', {'data': None})


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


@socketio.on('join')
def on_join(data):
    global gamestate

    rname = 'bomberman#{}'.format(data['room_num'])
    join_room(rname)
    server_logic.save_room(data['username'], rname)

    uname = data['username']
    plcode = server_logic.user_to_code(uname)
    gamestate[plcode] = [0, 1]

    print('{} has entered {}'.format(uname, rname))
    emit('notify_others', {'newplayer': uname}, room=rname)


@socketio.on('leave')
def on_leave(data):
    rname = 'bomberman#{}'.format(data['room_num'])
    leave_room(rname)
    server_logic.save_room(data['username'], None)

    print('{} has left {}'.format(data['username'], rname))


if __name__ == '__main__':
    tmp = _parser.parse_args()
    socketio.run(app, port=int(tmp.port))
