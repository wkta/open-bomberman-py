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

    freegfxid = 0

    COUNTDOWN_DUR = 7  # sec

    BOMB_DELAY = 3.8666  # sec
    # GRID_SIZE = 9

    GRID_WIDTH = 13
    GRID_HEIGHT = 11
    NB_PLAYERS = 2

    # convention: id player ira de 1000 à 2000
    ETYPE_BLOCK, ETYPE_WALL, ETYPE_POWERUP = range(2000, 2003)

    def __init__(self):
        super().__init__()

        # we set value to True when the spawn pos has been used
        xlimit = self.GRID_WIDTH-1
        ylimit = self.GRID_HEIGHT-1
        self._spawn_positions = {
            (0,       0):       False,
            (xlimit, ylimit): False,
            (0,       ylimit): False,
            (xlimit, 0):       False
        }

        # todo extend the gamestate
        # instead of having plcode <> pos we should use pos <> entitytype (-> storing walls, bombs, bonuses)
        # +lets use another variable for player positions, bc players can overlap
        self.gridstate = dict()
        self._plcode_to_pos = dict()
        self.bomblist = list()  # list of quads (i, j, plcode, timeinfo)

        self._last_spawn = None
        self._started_match = False
        self.match_winner = None
        self.gfxs = dict()

    def use_new_gfxid(self, plcode):
        gid = self.__class__.freegfxid
        self.__class__.freegfxid += 1
        self.gfxs[plcode] = gid
        return gid

    def load_level(self, filename):
        all_wpos = list()
        all_blocks = list()

        with open(filename, 'r') as f:
            matrx_type_obj = json.load(f)
            for j, row in enumerate(matrx_type_obj):
                for i, elt in enumerate(row):
                    if elt == 'W':
                        all_wpos.append((i, j))
                    elif elt == 'X':
                        all_blocks.append((i, j))

        for wpos in all_wpos:
            self.gridstate[wpos] = self.ETYPE_WALL
        for wpos in all_blocks:
            self.gridstate[wpos] = self.ETYPE_BLOCK

    def sync_state(self, other_world):
        grid_state, bombs = other_world.gridstate, other_world.bomblist
        # clear existing state
        self._plcode_to_pos.clear()
        del self.bomblist[:]

        self.gfxs = other_world.gfxs

        # replacing
        self.gridstate = grid_state
        self._refresh_pl_pos()
        self.bomblist.extend(bombs)

    def _refresh_pl_pos(self):
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
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
        if not self.has_match_started():
            return False

        k = tuple(future_pos)
        if k in self.gridstate:
            return False

        for elt in self.bomblist:
            if elt[0] == future_pos[0] and elt[1] == future_pos[1]:
                return False

        return True

    def has_match_started(self):
        return self._started_match

    def can_start(self, tnow):
        if len(self._plcode_to_pos) >= 2:
            if tnow - self._last_spawn > WorldModel.COUNTDOWN_DUR:
                return True
        return False

    def start_match(self):
        self._started_match = True

    def list_players(self):
        return list(self._plcode_to_pos.keys())

    def list_bombs(self):
        return self.bomblist

    def change_pl_position(self, plcode, ijpos: tuple):
        old_pos = self._plcode_to_pos[plcode]
        del self.gridstate[old_pos]

        self._plcode_to_pos[plcode] = ijpos
        self.gridstate[ijpos] = plcode

    def drop_bomb(self, plcode, timeinfo):
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
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                if ((i, j) in self.gridstate) and self.ETYPE_WALL == self.gridstate[(i, j)]:
                    tmp.append((i, j))
        return tmp

    def blocks_locations(self):
        tmp = list()
        for i in range(self.GRID_WIDTH):
            for j in range(self.GRID_HEIGHT):
                if ((i, j) in self.gridstate) and self.ETYPE_BLOCK == self.gridstate[(i, j)]:
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
                t_impacted_cell = self.gridstate[impacted_cell]
                if t_impacted_cell in (WorldModel.ETYPE_WALL, WorldModel.ETYPE_POWERUP):
                    del self.gridstate[impacted_cell]

                elif 1000 <= t_impacted_cell < 2000:  # is a player
                    dead_player = t_impacted_cell
                    del self._plcode_to_pos[dead_player]
                    del self.gridstate[impacted_cell]
                    if len(self._plcode_to_pos) < 2:  # one man standing...
                        self.match_winner = bomber

    @staticmethod
    def _comp_adjacent_cells(i, j):
        res = list()
        for offsetx in (-1, +1):
            if 0 <= i + offsetx < WorldModel.GRID_WIDTH:
                res.append((i+offsetx, j))
        for offsety in (-1, +1):
            if 0 <= j + offsety < WorldModel.GRID_HEIGHT:
                res.append((i, j+offsety))
        return res

    def spawn_player(self, plcode, tnow):
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

        self._last_spawn = tnow

        initpos = random.choice(free_possib)
        self._spawn_positions[initpos] = True

        self._plcode_to_pos[plcode] = initpos
        self.gridstate[initpos] = plcode

    def player_location(self, plcode):
        return list(self._plcode_to_pos[plcode])

    def getgfxid(self, plcode):
        return self.gfxs[plcode]

    def serialize(self):
        # NEITHER players pos, NOR timeinfo on bombs areserialized/!\
        res = str(self.gridstate)
        res += '|'
        # gfxs
        res += str(self.gfxs)
        res += '|'

        res += str(self.bomblist)
        res += '|'
        if self._started_match:
            res += '1'
        else:
            res += '0'
        if self.match_winner is None:
            res += '|0'
        else:
            res += '|' + str(self.match_winner)
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
        gfxs = eval(tmp[1])
        obj.gfxs =gfxs

        li = eval(tmp[2])

        obj.gridstate = dico
        obj.bomblist = li
        obj._refresh_pl_pos()
        if tmp[3] == '1':
            obj._started_match = True
        else:
            obj._started_match = False
        if tmp[4] == '0':
            pass
        else:
            obj.match_winner = int(tmp[3])

        return obj


if __name__ == '__main__':
    print('saleu')
    monde = WorldModel()

    monde.spawn_player(1000, 15897312)
    monde.spawn_player(1001, 143987.8)
    monde.spawn_player(1002, 1534897)

    monde.drop_bomb(1002, time.time()+3.8)

    val_s = monde.serialize()

    copie = WorldModel.deserialize(val_s)
    print(copie.serialize())
