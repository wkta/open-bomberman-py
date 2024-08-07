from WorldModel import WorldModel
from coremon_main import CogObject
from def_gevents import MyEvTypes


class WorldSubjectMod(CogObject):
    """
    this class is a WRAPPER for one WorldModel instance,
    it simply allows event posting so the WorldModel can be viewed on screen
    """

    def __init__(self):
        super().__init__()
        self.is_sync = False
        self.irepr = WorldModel()

    def getgfxid(self, plcode):
        return self.irepr.getgfxid(plcode)

    @property
    def gridsize(self):
        return WorldModel.GRID_WIDTH, WorldModel.GRID_HEIGHT

    def tag_gs_change(self):
        self.pev(MyEvTypes.BombsetChanges, info=self.irepr.bomb_locations())
        self.pev(MyEvTypes.PlayerMoves)

    # était utilisé avant websockets
    # def load_state(self, serial):
    #     if glvars.DEV_MODE:
    #         print('loading new state in LocalWorld: serial= ', end='')
    #         print(serial)
    #
    #     self.gameworld.load_state(serial)
    #     self.pev(MyEvTypes.WorldChanges, newstate=self.gameworld.state)
