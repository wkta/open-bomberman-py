import glvars
import socketio_bridge
from PlayerAction import PlayerAction
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver


class MultiplayerGmCtrl(EventReceiver):

    def __init__(self):
        super().__init__()

    def proc_event(self, ev, source=None):

        if ev.type == PygameBridge.KEYDOWN:
            self._process_keypress(ev)

    def _process_keypress(self, ev):

        if ev.key == PygameBridge.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)
            return

        if ev.key == PygameBridge.K_SPACE:
            act = PlayerAction(glvars.local_pl_code, PlayerAction.T_BOMB)
            socketio_bridge.push_action(act)
            return

        direct = None
        if ev.key == PygameBridge.K_RIGHT:
            direct = 0
        elif ev.key == PygameBridge.K_UP:
            direct = 1
        elif ev.key == PygameBridge.K_LEFT:
            direct = 2
        elif ev.key == PygameBridge.K_DOWN:
            direct = 3

        if direct is not None:
            act = PlayerAction(glvars.local_pl_code, PlayerAction.T_MOVEMENT, direction=direct)
            socketio_bridge.push_action(act)
