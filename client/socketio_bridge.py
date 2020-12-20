import socketio

import basiques
import coremon_main
import glvars
from coremon_main import EventManager, CgmEvent
from def_gevents import MyEvTypes, SERV_COMM_KEY


if glvars.NEED_NETW_DEBUG:
    sio = socketio.Client(logger=True, engineio_logger=True)
else:
    sio = socketio.Client()


# ------------------ handy actuators ------------------
def enable():
    sio.connect('http://{}:{}'.format(glvars.host, glvars.port))  # => serv_welcome, serv_allrooms


def disable():
    sio.disconnect()


def join_room(user, num):
    sio.emit('join', {'username': user, 'room_num': int(num)})  # => serv_countdown_reset, serv_gamestarts


def push_action(act_obj):
    print('** pushing action to server using ws: act_obj= {}'.format(act_obj))
    serial = act_obj.serialize()
    print('serial= '+serial)
    sio.emit('push_action', serial)
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
@sio.event
def server_notification(data):
    """
    generic socketio event, using this event we wrap then unwrap
    coremon_engine custom game events.

    This procedure ALWAYS posts a CgmEvent object using the EventManager
    """

    # unpack custom game event name
    lowercase_style_evtname = data[SERV_COMM_KEY]
    del data[SERV_COMM_KEY]
    cc_style_evtname = basiques.to_camel_case(lowercase_style_evtname)

    adhoc_expr = 'CgmEvent(MyEvTypes.{}, **data)'.format(cc_style_evtname)
    evt = eval(adhoc_expr)
    print('   [NETW] >>> {}'.format(evt))
    EventManager.instance().post(evt)


# @sio.event
# def death(data):
#     print('received a death message!')


@sio.on('my message')
def on_message(data):
    print('I received a message!')


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
