import glvars
from bm_defs import MyEvTypes
from coremon_main import CogObject
from mirror.WorldModel import WorldModel


class LocalWorld(CogObject):
    """
    wrapper for WorldModel instance, with events enabled
    """
    
    def __init__(self):
        super().__init__()
        self.gameworld = WorldModel()

    def set_pos_from_netw(self, plcode, ij_pos):
        self.gameworld.state[plcode] = ij_pos

        self.pev(MyEvTypes.WorldChanges, newstate=self.gameworld.state)

    # était utilisé avant websockets
    # def load_state(self, serial):
    #     if glvars.DEV_MODE:
    #         print('loading new state in LocalWorld: serial= ', end='')
    #         print(serial)
    #
    #     self.gameworld.load_state(serial)
    #     self.pev(MyEvTypes.WorldChanges, newstate=self.gameworld.state)

    @property
    def gridsize(self):
        return WorldModel.GRID_SIZE
