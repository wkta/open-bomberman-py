import socketio_bridge
from app.multip_game.ctrl import MultipGameCtrl
from app.multip_game.view import MultipGameView
from coremon_main import BaseGameState
from transversal.LocalWorld import LocalWorld


class MultipGameState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        print('entering ClickChallg state...')
        self.m = LocalWorld()

        self.v = MultipGameView(self.m)
        self.v.turn_on()

        self.c = MultipGameCtrl(self.m)
        self.c.turn_on()
        socketio_bridge.enable()

    def release(self):
        print('ClickChallg state released.')
        self.c.turn_off()
        self.c = None
        self.v.turn_off()
        self.v = None

        socketio_bridge.disable()
