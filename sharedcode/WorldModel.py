import json
import random
import time


class WorldModel:
    """
    Models the world where players can move...
    Describes most of the abstract game logic
        -> what are spawn positions?
        -> where are walls?
        -> what's the delay before bomb explosions?
        -> who dies when a bomb explodes?
    """

    BOMB_DELAY = 3.8666  # sec
    GRID_SIZE = 9
    NB_PLAYERS = 2

    # convention: id player ira de 1000 à 2000
    ETYPE_WALL, ETYPE_POWERUP = range(2000, 2002)

    def __init__(self):
        super().__init__()

        # we set value to True when the spawn pos has been used
        mxcoord = self.GRID_SIZE-1
        self._spawn_positions = {
            (0,       0):       False,
            (mxcoord, mxcoord): False,
            (0,       mxcoord): False,
            (mxcoord, 0):       False
        }

        # todo extend the gamestate
        # instead of having plcode <> pos we should use pos <> entitytype (-> storing walls, bombs, bonuses)
        # +lets use another variable for player positions, bc players can overlap
        self.gridstate = dict()
        self._plcode_to_pos = dict()
        self.bomblist = list()  # list of quads (i, j, plcode, timeinfo)

    def load_level(self, filename):
        all_wpos = list()

        with open(filename, 'r') as f:
            matrx_type_obj = json.load(f)
            for j, row in enumerate(matrx_type_obj):
                for i, elt in enumerate(row):
                    if elt == 'W':
                        all_wpos.append((i, j))

        for wpos in all_wpos:
            self.gridstate[wpos] = self.ETYPE_WALL

    def sync_state(self, other_world):
        grid_state, bombs = other_world.gridstate, other_world.bomblist
        # clear existing state
        self._plcode_to_pos.clear()
        del self.bomblist[:]

        # replacing
        self.gridstate = grid_state
        self._refresh_pl_pos()
        self.bomblist.extend(bombs)

    def _refresh_pl_pos(self):
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if (i, j) not in self.gridstate:
                    continue
                tmp = self.gridstate[(i, j)]
                if 1000 <= tmp < 2000:
                    self._plcode_to_pos[tmp] = (i, j)

    def all_players_position(self):
        """
        :return: list of triplets in the form of: plcode, i, j
        """
        res = list()
        for plcode, pos in self._plcode_to_pos.items():
            triplet = (plcode, pos[0], pos[1])
            res.append(triplet)
        return res

    # * shared on both sides *
    def can_walk(self, future_pos):
        k = tuple(future_pos)
        if k in self.gridstate:
            return False
        for elt in self.bomblist:
            if elt[0] == future_pos[0] and elt[1] == future_pos[1]:
                return False
        return True

    def list_bombs(self):
        return self.bomblist

    def change_pl_position(self, plcode, ijpos: tuple):
        old_pos = self._plcode_to_pos[plcode]
        del self.gridstate[old_pos]

        self._plcode_to_pos[plcode] = ijpos
        self.gridstate[ijpos] = plcode

    def drop_bomb(self, plcode, timeinfo=None):
        i, j = self._plcode_to_pos[plcode]
        self.bomblist.append((i, j, plcode, timeinfo))

    def remove_bomb(self, x, y):
        idx = None
        for k, elt in enumerate(self.bomblist):
            if elt[0] == x and elt[1] == y:
                idx = k
                break
        del self.bomblist[idx]

    def bomb_locations(self):
        res = list()
        for elt in self.bomblist:
            res.append((elt[0], elt[1]))
        return res

    def wall_locations(self):
        tmp = list()
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if ((i, j) in self.gridstate) and self.ETYPE_WALL == self.gridstate[(i, j)]:
                    tmp.append((i, j))
        return tmp

    # -----------------------
    #  Triggered server-side

    def trigger_explosion(self, ij_pos):
        """
        game logic: what is the effect of an exploding bomb?

        :param ij_pos:
        :return:
        """
        i, j = ij_pos
        bomber = None
        idx = None
        for k, elt in enumerate(self.bomblist):
            if elt[0] == i and elt[1] == j:
                idx = k
                bomber = elt[2]
                break
        del self.bomblist[idx]

        for impacted_cell in WorldModel._comp_adjacent_cells(i, j):
            if impacted_cell in self.gridstate:
                if self.gridstate[impacted_cell] in (self.ETYPE_WALL, self.ETYPE_POWERUP):
                    del self.gridstate[impacted_cell]
                    print('removing content of {}'.format(impacted_cell))

    @staticmethod
    def _comp_adjacent_cells(i, j):
        res = list()
        for offsetx in (-1, +1):
            if 0 <= i + offsetx < WorldModel.GRID_SIZE:
                res.append((i+offsetx, j))
        for offsety in (-1, +1):
            if 0 <= j + offsety < WorldModel.GRID_SIZE:
                res.append((i, j+offsety))
        return res

    def spawn_player(self, plcode):
        # we list what positions are already taken, to compute what pos. are free
        free_possib = list(self._spawn_positions.keys())
        to_prune_possib = set()
        for p in free_possib:
            if self._spawn_positions[p]:
                to_prune_possib.add(p)
        for elt in to_prune_possib:
            free_possib.remove(elt)

        if len(free_possib) == 0:
            raise ValueError('no spawn position left for spawning player!')

        initpos = random.choice(free_possib)
        self._spawn_positions[initpos] = True

        self._plcode_to_pos[plcode] = initpos
        self.gridstate[initpos] = plcode

    def player_location(self, plcode):
        return list(self._plcode_to_pos[plcode])

    def serialize(self):
        # NEITHER players pos, NOR timeinfo on bombs areserialized/!\
        res = str(self.gridstate)
        res += '|'
        res += str(self.bomblist)
        return res

    # -----------------------
    #  Triggered client-side
    def __getitem__(self, xy_info):
        x, y = xy_info
        return self.gridstate[x][y]

    @classmethod
    def deserialize(cls, serial):
        obj = cls()
        tmp = serial.split('|')
        dico = eval(tmp[0])
        li = eval(tmp[1])

        obj.gridstate = dico
        obj.bomblist = li
        obj._refresh_pl_pos()

        return obj


if __name__ == '__main__':
    print('saleu')
    monde = WorldModel()

    monde.spawn_player(1000)
    monde.spawn_player(1001)
    monde.spawn_player(1002)

    monde.drop_bomb(1002, time.time()+3.8)

    val_s = monde.serialize()

    copie = WorldModel.deserialize(val_s)
    print(copie.serialize())
