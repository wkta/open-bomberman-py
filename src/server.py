from flask import Flask, render_template
from flask_socketio import SocketIO
import argparse
from flask import Flask, jsonify
import hashlib
import json


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
_parser = argparse.ArgumentParser(add_help=False)
_parser.add_argument('-h', '--host', help='specify host', required=True)
_parser.add_argument('-p', '--port', help='specify port', required=True)


cpt = 0
gamestate = dict()
BSUP = 8
gs_init = False


def loadstate():
    global gamestate, gs_init
    with open('gamestate.json', 'r') as fptr:
        obj = json.load(fptr)

    gamestate.clear()
    for k, v in obj.items():
        gamestate[int(k)] = v
    gs_init = True


@app.route('/')
def index():
    global cpt
    cpt += 1
    return "hello there, req #{}".format(cpt)


@app.route('/move/<plcode>/<direct>')
def move(plcode, direct):  # can use with direct==-1 to just query the position...
    global gs_init, BSUP
    if not gs_init:
        loadstate()

    k = int(plcode)
    d = int(direct)
    if d == 0:
        gamestate[k][0] += 1
        if gamestate[k][0] > BSUP:
            gamestate[k][0] = BSUP

    elif d == 1:
        gamestate[k][1] -= 1
        if gamestate[k][1] < 0:
            gamestate[k][1] = 0

    elif d == 2:
        gamestate[k][0] -= 1
        if gamestate[k][0] < 0:
            gamestate[k][0] = 0

    elif d == 3:
        gamestate[k][1] += 1
        if gamestate[k][1] > BSUP:
            gamestate[k][1] = BSUP

    return jsonify(gamestate[k])


@app.route('/statesig')
def statesig():
    global gs_init, gamestate
    if not gs_init:
        loadstate()

    m = hashlib.sha224()
    clients = list(gamestate.keys())
    clients.sort()
    for c in clients:
        m.update('{}{}{}'.format(c, gamestate[c][0], gamestate[c][1]).encode('ascii'))
    return jsonify(m.hexdigest())


@app.route('/save')
def save():
    pass


tmp = _parser.parse_args()
print(tmp.host)
print(tmp.port)
app.run(host=tmp.host, port=tmp.port)
