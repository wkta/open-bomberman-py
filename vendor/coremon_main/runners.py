import time

import pygame
from pygame import constants

from coremon_main.StContainer import StContainer
from coremon_main.structures import Stack
from ._events import EngineEvTypes, EventManager, EventReceiver


class VanillaGameCtrl(EventReceiver):

    def __init__(self, max_fps=60):
        super().__init__(True)  # is sticky? YES
        self._running = True
        self._manager = EventManager.instance()
        self._clock = pygame.time.Clock()
        self.max_fps = max_fps
        self._autoquit = True

    def set_autoquit(self, bool_val=True):
        assert isinstance(bool_val, bool)
        self._autoquit = bool_val

    def _halt_the_game(self):
        self._running = False

    def proc_event(self, ev, source):
        if self._autoquit:
            if ev.type == constants.QUIT:
                self._halt_the_game()
        if ev.type == EngineEvTypes.GAMEENDS:
            self._halt_the_game()

    def loop(self):
        while self._running:
            self.pev(EngineEvTypes.LOGICUPDATE)
            self.pev(EngineEvTypes.PAINT)
            self._manager.update()

            pygame.display.flip()
            self._clock.tick(self.max_fps)


class HeadlessRunnerCtrl(VanillaGameCtrl):
    def __init__(self, freq_exec_s):
        super().__init__()
        self.max_fps = None
        self._freq = freq_exec_s

    def loop(self):
        while self._running:
            time.sleep(self._freq)
            self.pev(EngineEvTypes.LOGICUPDATE)
            self._manager.update()


class StackBasedGameCtrl(VanillaGameCtrl):

    def __init__(self, gamestates_enum, init_gs_id, max_fps=60):
        self._id = 27391
        # construction de tous les états...
        self._st_container = StContainer.instance()
        self._st_container.setup(gamestates_enum)

        super().__init__(max_fps)
        self.__state_stack = Stack()  # a kind of embedded game model
        self.__state_stack.push(init_gs_id)

        # calling enter method...
        self._st_container.retrieve(init_gs_id).enter()

    def get_curr_state_ident(self):
        return self.__state_stack.peek()

    # redefinition
    def _halt_the_game(self):
        while self.get_curr_state_ident() is not None:
            self._pop_state()

    def proc_event(self, ev, source):
        super().proc_event(ev, source)

        if ev.type == EngineEvTypes.PUSHSTATE:
            state_obj = self._st_container.retrieve(ev.state_ident)
            self._push_state(state_obj)

        elif ev.type == EngineEvTypes.POPSTATE:
            self._pop_state()

        elif ev.type == EngineEvTypes.CHANGESTATE:
            state_obj = self._st_container.retrieve(ev.state_ident)
            self._change_state(state_obj)

    # --- ---
    #  MÉTIER
    # --- ---
    def _push_state(self, state_obj):
        tmp = self.__state_stack.peek()
        curr_state = self._st_container.retrieve(tmp)
        curr_state.pause()

        self.__state_stack.push(state_obj.get_id())
        state_obj.enter()

    def _pop_state(self):
        self.__only_the_pop_part()
        # follow-up
        if self.__state_stack.count() == 0:
            self._running = False
        else:
            tmp = self.__state_stack.peek()
            state_obj = self._st_container.retrieve(tmp)
            state_obj.resume()

    def _change_state(self, state_obj):
        self.__only_the_pop_part()
        # follow-up
        self.__state_stack.push(state_obj.get_id())
        state_obj.enter()

    # private method. Warning! never call this method without some kind of follow-up!
    def __only_the_pop_part(self):
        tmp = self.__state_stack.pop()
        state_obj = self._st_container.retrieve(tmp)
        state_obj.release()
