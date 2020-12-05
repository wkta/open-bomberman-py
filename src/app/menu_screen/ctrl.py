from app.menu_screen.model import MenuScreenModel
from bm_defs import GameStates
from coremon_main import PygameBridge, EngineEvTypes, EventReceiver


class MenuScreenCtrl(EventReceiver):

    def __init__(self, mod):
        super().__init__()
        self._mod = mod

    def proc_event(self, ev, source=None):
        if ev.type == PygameBridge.KEYDOWN:
            if ev.key == PygameBridge.K_DOWN:
                self._mod.incr_selection()
            elif ev.key == PygameBridge.K_UP:
                self._mod.decr_selection()
            elif ev.key == PygameBridge.K_RETURN or PygameBridge.K_KP_ENTER:
                if self._mod.selection == MenuScreenModel.QUIT_OPTION:
                    self.pev(EngineEvTypes.GAMEENDS)
                else:
                    self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.ClickChallg)

        elif ev.type == PygameBridge.MOUSEBUTTONUP:
            print('pushing the ClickChallg state onto the stack...')
            self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.ClickChallg)
