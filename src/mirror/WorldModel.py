import json


class WorldModel:

    GRID_SIZE = 9

    def __init__(self):
        super().__init__()
        self.state = dict()

    def load_state(self, json_str):
        print('model synchronizing...')
        self.state = {1: json.loads(json_str)}
