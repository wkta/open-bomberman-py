from coremon_main import CogObject
from defs_bombm import MyEvTypes
from mirror.WorldModel import WorldModel


class LocalWorld(CogObject):
    """
    wrapper for WorldModel instance, with events enabled
    """

    def __init__(self):
        super().__init__()
        self.is_sync = False
        self.irepr = WorldModel()

    @property
    def gridsize(self):
        return WorldModel.GRID_SIZE

    def set_pos_from_netw(self, plcode, ij_pos):
        self.irepr.state[plcode] = ij_pos
        self.pev(MyEvTypes.PlayerMoves)

    # était utilisé avant websockets
    # def load_state(self, serial):
    #     if glvars.DEV_MODE:
    #         print('loading new state in LocalWorld: serial= ', end='')
    #         print(serial)
    #
    #     self.gameworld.load_state(serial)
    #     self.pev(MyEvTypes.WorldChanges, newstate=self.gameworld.state)
