import socketio

import coremon_main
from bm_defs import MyEvTypes
from coremon_main import EventManager, CgmEvent

NEED_DEBUG = False
if NEED_DEBUG:
    sio = socketio.Client(logger=True, engineio_logger=True)
else:
    sio = socketio.Client()


# ------------------ handy actuators ------------------
def enable():
    sio.connect('http://localhost:8577')


def disable():
    sio.disconnect()


def push_movement(plcode, direct):
    margs = [plcode, direct]
    print('** pushing mvt to server using ws | margs will be: {}, {}**'.format(1, direct))
    sio.emit('pushmove', {'margs': margs})


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

    EventManager.instance().post(CgmEvent(MyEvTypes.PlayerMoved, plcode=code, new_pos=newpos))


@sio.event
def death(data):
    print('received a death message!')


@sio.on('serv response')
def serv_response(data):
    print(' >> server >> {}'.format(data))


@sio.on('my message')
def on_message(data):
    print('I received a message!')


def joinroom():
    sio.emit('join', {})


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
