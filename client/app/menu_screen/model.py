from def_gevents import MyEvTypes
from coremon_main import CogObject


class MenuScreenModel(CogObject):

    SOLO_CODE, MULTI_CODE, NETWCONFIG_CODE, QUIT_OPTION = range(4)

    def __init__(self):
        super().__init__()
        self._selected_mode = 0
        self.__nb_modes = 4

    @property
    def nb_modes(self):
        return self.__nb_modes

    @property
    def selection(self):
        return self._selected_mode

    def incr_selection(self):
        self._selected_mode += 1
        self._selected_mode = self._selected_mode % self.nb_modes
        self.pev(MyEvTypes.PlSelectsMode, k=self._selected_mode)

    def decr_selection(self):
        self._selected_mode -= 1
        if self._selected_mode < 0:
            self._selected_mode = self.nb_modes-1
        self.pev(MyEvTypes.PlSelectsMode, k=self._selected_mode)
