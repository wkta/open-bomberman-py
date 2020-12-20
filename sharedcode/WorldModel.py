import json


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
    ETYPE_WALL, ETYPE_BOMB = range(189237, 189237+2)

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
        self._grid_state = dict()
        self._init_level()

        self._pl_positions = dict()
        self._bomb_infos = dict()  # assoc position(int,int) <> date when planted(float)

    def _init_level(self):
        all_wpos = [
            (1, 1),
            (2, 1),
            (3, 1),

            (7, 7),
            (6, 7),
            (5, 7)
        ]
        for wpos in all_wpos:
            self._grid_state[wpos] = self.ETYPE_WALL

    def list_players(self):
        """
        :return: list of triplets plcode, i, j
        """
        res = list()

        mecs = list(self._pl_positions.keys())
        for m in mecs:
            i, j = self._pl_positions[m]
            triplet = (m, i, j)
            res.append(triplet)

        return res

    # * shared on both sides *

    def change_pl_position(self, plcode, ijpos):
        self._pl_positions[plcode] = ijpos

    def add_bomb(self, x, y, timeinfo=None):
        self._bomb_infos[(x, y)] = timeinfo
        self._grid_state[(x, y)] = self.ETYPE_BOMB

    def remove_bomb(self, x, y):
        self._grid_state[(x, y)] = None
        del self._bomb_infos[(x, y)]

    def bomb_locations(self):
        return list(self._bomb_infos.keys())

    def wall_locations(self):
        tmp = list()
        for i in range(self.GRID_SIZE):
            for j in range(self.GRID_SIZE):
                if ((i, j) in self._grid_state) and self.ETYPE_WALL == self._grid_state[(i, j)]:
                    tmp.append((i, j))
        return tmp

    def get_bomb_infos(self):
        return dict(self._bomb_infos)

    # -----------------------
    #  Triggered server-side
    def consume_spawn(self, plcode):
        res = None
        for spawn_p in self._spawn_positions:
            if self._spawn_positions[spawn_p]:
                continue

            self._spawn_positions[spawn_p] = True
            self._pl_positions[plcode] = spawn_p
            res = spawn_p
            break
        return res

    def player_location(self, plcode):
        return list(self._pl_positions[plcode])

    def serialize(self):
        # NEITHER players pos, NOR timeinfo on bombs areserialized/!\
        return json.dumps(self._grid_state)

    # -----------------------
    #  Triggered client-side
    def __getitem__(self, xy_info):
        x, y = xy_info
        return self._grid_state[x][y]

    @classmethod
    def deserialize(cls, json_serial):
        obj = cls()
        d = json.loads(json_serial)
        assert cls.NB_PLAYERS == len(d)
        obj._grid_state = d
        return obj
