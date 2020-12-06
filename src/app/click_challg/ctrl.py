import time

import glvars
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver


code_do_synchro = 998767


class ClickChallgCtrl(EventReceiver):

    def __init__(self, mod):
        super().__init__()
        self._last_sync = None
        self._mod = mod

    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            if self._last_sync is None:
                self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/move/1/-1', num=code_do_synchro)
                self._last_sync = time.time()

            else:
                tnow = time.time()
                dt = tnow - self._last_sync
                if dt > 5.0:  # polling, freq 5sec
                    self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/move/1/-1', num=code_do_synchro)
                    self._last_sync = tnow

        elif ev.type == EngineEvTypes.INGOINGNETW:
            if ev.num == code_do_synchro:
                self._mod.load_state(ev.msg)

        elif ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_ESCAPE:
                self.pev(EngineEvTypes.POPSTATE)

            elif ev.key == PygameBridge.K_RIGHT:
                self.mvt_serv_side(0)
            elif ev.key == PygameBridge.K_UP:
                self.mvt_serv_side(1)
            elif ev.key == PygameBridge.K_LEFT:
                self.mvt_serv_side(2)
            elif ev.key == PygameBridge.K_DOWN:
                self.mvt_serv_side(3)

    def mvt_serv_side(self, direct):
        nimp = code_do_synchro // 2
        self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/move/1/{}'.format(direct), num=nimp)
