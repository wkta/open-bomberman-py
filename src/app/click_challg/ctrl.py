import glvars
from bm_defs import MyEvTypes
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver
import socketio_bridge


code_do_synchro = 998767


class ClickChallgCtrl(EventReceiver):

    def __init__(self, mod):
        super().__init__()
        self._is_sync = False

        self._last_sync = None
        self._mod = mod

    def proc_event(self, ev, source=None):
        dirty_local_pl_code = glvars.local_pl_code

        if ev.type == EngineEvTypes.LOGICUPDATE:
            if not self._is_sync:
                socketio_bridge.joinroom()

                for pl in glvars.allplayers:
                    socketio_bridge.push_movement(pl, -1)  # provoque refresh position
                self._is_sync = True

            # -desactivé depuis quon utilise WS
            # if self._last_sync is None:
            #     self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/move/1/-1', num=code_do_synchro)
            #     self._last_sync = time.time()
            #
            # else:
            #     tnow = time.time()
            #     dt = tnow - self._last_sync
            #     if dt > 5.0:  # polling, freq 5sec
            #         self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/move/1/-1', num=code_do_synchro)
            #         self._last_sync = tnow

        elif ev.type == MyEvTypes.PlayerMoved:
            print('ctrler receiving PlayerMoved evnt')
            self._mod.set_pos_from_netw(ev.plcode, ev.new_pos)

        elif ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_ESCAPE:
                self.pev(EngineEvTypes.POPSTATE)

            elif ev.key == PygameBridge.K_RIGHT:
                ClickChallgCtrl.mvt_serv_side(dirty_local_pl_code, 0)
            elif ev.key == PygameBridge.K_UP:
                ClickChallgCtrl.mvt_serv_side(dirty_local_pl_code, 1)
            elif ev.key == PygameBridge.K_LEFT:
                ClickChallgCtrl.mvt_serv_side(dirty_local_pl_code, 2)
            elif ev.key == PygameBridge.K_DOWN:
                ClickChallgCtrl.mvt_serv_side(dirty_local_pl_code, 3)

    @staticmethod
    def mvt_serv_side(local_plcode, direct):
        # - the old way
        # nimp = code_do_synchro // 2
        # self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/move/1/{}'.format(direct), num=nimp)

        # - the new way
        socketio_bridge.push_movement(local_plcode, direct)
