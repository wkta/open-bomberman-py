import socketio

import coremon_main
import glvars
from coremon_main import EventManager, CgmEvent
from defs_bombm import MyEvTypes


NEED_DEBUG = False
if NEED_DEBUG:
    sio = socketio.Client(logger=True, engineio_logger=True)
else:
    sio = socketio.Client()


# ------------------ handy actuators ------------------
def enable():
    sio.connect('http://{}:{}'.format(glvars.host, glvars.port))


def disable():
    sio.disconnect()


def push_movement(username, direct):
    print('** pushing mvt to server using ws | arg will be: {} **'.format([username, direct] ))
    sio.emit('pushmove', [username, direct])
    # triggers the server to send player_moved


# ------------------ remote events(generic) ------------------
@sio.event
def connect():
    print("I'm connected!")
    # sio.emit('my message', {'foo': 'bar'})


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


# ------------------ remote events(specific) ------------------
@sio.on('player_moved')
def handle_player_moved(data):
    # retrieves the new player pos
    code = int(data['code'])
    newpos = data['newpos']
    print('**receiving feedback from server: code= {}, newpos={} **'.format(code, newpos))

    EventManager.instance().post(CgmEvent(MyEvTypes.GamestateServFeedback, plcode=code, new_pos=newpos))


@sio.event
def death(data):
    print('received a death message!')


@sio.on('connection_ok')
def serv_response(username):
    print('connection_ok, username= {}'.format(username))
    EventManager.instance().post(CgmEvent(MyEvTypes.ServerLoginOk, username=username))


@sio.on('notify_others')
def notify_others(data):
    print('local client knows that plyer {} entered current room'.format(data['newplayer']))
    EventManager.instance().post(
        CgmEvent(MyEvTypes.OtherGuyCame, username=data['newplayer'])
    )



@sio.on('my message')
def on_message(data):
    print('I received a message!')


def joinroom(user, num):
    sio.emit('join', {'username': user, 'room_num': int(num)})


if __name__ == '__main__':
    coremon_main.init_headless()
    # test serveur: on se connecte
    enable()
    print('(1) connecting... My sid is', sio.sid)
    print()

    print('[pause 3s]')
    sio.sleep(3)

    print('(2) sending pushmove')
    sio.emit('pushmove', {'margs': [1, 0]})

    print('[pause 3s]')
    sio.sleep(3)

    print('(3) disconnecting')
    disable()
    print()

    EventManager.instance().dump_event_queue()
    print('done.')
