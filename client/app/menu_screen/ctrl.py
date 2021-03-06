import glvars
from app.menu_screen.model import MenuScreenModel
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver
from def_gamestates import GameStates


class MenuScreenCtrl(EventReceiver):

    def __init__(self, mod):
        super().__init__()
        self._mod = mod

    def proc_event(self, ev, source=None):

        if ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_ESCAPE:
                self.pev(EngineEvTypes.GAMEENDS)

            elif ev.key == PygameBridge.K_DOWN:
                self._mod.incr_selection()

            elif ev.key == PygameBridge.K_UP:
                self._mod.decr_selection()

            elif ev.key in (PygameBridge.K_RETURN, PygameBridge.K_KP_ENTER):

                if self._mod.selection == MenuScreenModel.QUIT_OPTION:
                    self.pev(EngineEvTypes.GAMEENDS)

                elif self._mod.selection == MenuScreenModel.NETWCONFIG_CODE:
                    self.pev(EngineEvTypes.OUTGOINGNETW, host=glvars.host, resource='/', num=666)

                elif self._mod.selection == MenuScreenModel.SOLO_CODE:
                    glvars.local_pl_code = 1
                    self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.MultipGame)

                elif self._mod.selection == MenuScreenModel.MULTI_CODE:
                    glvars.local_pl_code = 2
                    self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.MultipGame)

        elif ev.type == EngineEvTypes.INGOINGNETW:
            print('*** debug netw ***')
            print('receiving msg')
            print('msg= '+str(ev.msg))
            print('num= '+str(ev.num))
