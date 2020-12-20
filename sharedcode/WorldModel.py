import json


class WorldModel:
    """
    the world where players can move...
    """

    GRID_SIZE = 9
    NB_PLAYERS = 2

    def __init__(self):
        super().__init__()
        self.state = dict()
        self.bombs = set()

    def list_players(self):
        return range(1, self.NB_PLAYERS+1)

    def __getitem__(self, k_index):
        return self.state[int(k_index)]

    def add_bomb(self, x, y):
        self.bombs.add((x, y))

    def remove_bomb(self, x, y):
        self.bombs.remove((x, y))

    @classmethod
    def deserialize(cls, json_serial):
        obj = cls()
        d = json.loads(json_serial)
        assert cls.NB_PLAYERS == len(d)
        obj.state = d
        return obj

    def serialize(self):
        return json.dumps(self.state)
