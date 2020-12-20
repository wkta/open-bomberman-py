from coremon_main import CogObject
from def_gevents import MyEvTypes
from WorldModel import WorldModel


class WorldSubjectMod(CogObject):
    """
    this class is a WRAPPER for one WorldModel instance,
    it simply allows event posting so the WorldModel can be viewed on screen
    """

    def __init__(self):
        super().__init__()
        self.is_sync = False
        self.irepr = WorldModel()

    @property
    def gridsize(self):
        return WorldModel.GRID_SIZE

    def set_pos_from_netw(self, plcode, ij_pos):
        self.irepr.change_pl_position(plcode, ij_pos)
        self.pev(MyEvTypes.PlayerMoves)

    # - redefining...
    def add_bomb(self, x, y):
        print('subject model: bomb added')
        self.irepr.add_bomb(x, y)
        self.pev(MyEvTypes.BombsetChanges, info=self.irepr.list_bombs())

    def remove_bomb(self, x, y):
        print('subject model: bomb removed')
        self.irepr.remove_bomb(x, y)
        self.pev(MyEvTypes.BombsetChanges, info=self.irepr.list_bombs())

    # était utilisé avant websockets
    # def load_state(self, serial):
    #     if glvars.DEV_MODE:
    #         print('loading new state in LocalWorld: serial= ', end='')
    #         print(serial)
    #
    #     self.gameworld.load_state(serial)
    #     self.pev(MyEvTypes.WorldChanges, newstate=self.gameworld.state)
