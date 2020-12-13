import glvars
import socketio_bridge
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver
from defs_bombm import MyEvTypes
from transversal.LocalWorld import LocalWorld


code_do_synchro = 998767


class MultipGameCtrl(EventReceiver):

    def __init__(self, mod: LocalWorld):
        super().__init__()

        self._last_sync = None
        self._mod = mod

    def proc_event(self, ev, source=None):
        dirty_local_pl_code = glvars.local_pl_code

        if ev.type == EngineEvTypes.LOGICUPDATE:
            if not self._mod.is_sync:
                socketio_bridge.joinroom()

                for pl in self._mod.irepr.list_players():
                    socketio_bridge.push_movement(pl, -1)  # provoque refresh position

                self._mod.is_sync = True

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

        elif ev.type == MyEvTypes.GamestateServFeedback:
            print('MultipGame controler has detected a GamestateServFeedback evt')
            self._mod.set_pos_from_netw(ev.plcode, ev.new_pos)

        elif ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_ESCAPE:
                self.pev(EngineEvTypes.POPSTATE)

            elif ev.key == PygameBridge.K_RIGHT:
                MultipGameCtrl.mvt_serv_side(dirty_local_pl_code, 0)
            elif ev.key == PygameBridge.K_UP:
                MultipGameCtrl.mvt_serv_side(dirty_local_pl_code, 1)
            elif ev.key == PygameBridge.K_LEFT:
                MultipGameCtrl.mvt_serv_side(dirty_local_pl_code, 2)
            elif ev.key == PygameBridge.K_DOWN:
                MultipGameCtrl.mvt_serv_side(dirty_local_pl_code, 3)

    @staticmethod
    def mvt_serv_side(local_plcode, direct):
        # - the old way
        # nimp = code_do_synchro // 2
        # self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/move/1/{}'.format(direct), num=nimp)

        # - the new way
        socketio_bridge.push_movement(local_plcode, direct)
