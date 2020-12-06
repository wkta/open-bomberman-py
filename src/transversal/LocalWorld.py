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

    def load_state(self, serial):
        self.gameworld.load_state(serial)
        self.pev(MyEvTypes.WorldChanges, newstate=self.gameworld.state)

    @property
    def gridsize(self):
        return WorldModel.GRID_SIZE
