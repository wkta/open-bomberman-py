import socketio_bridge
from app.multip_game.MultiplayerGmCtrl import MultiplayerGmCtrl
from app.multip_game.PacketRecvCtrl import PacketRecvCtrl
from app.multip_game.view import MultipGameView
from coremon_main import BaseGameState
from transversal.WorldSubjectMod import WorldSubjectMod


class MultipGameState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None
        self.c2 = None

    def enter(self):
        print('entering ClickChallg state...')
        self.m = WorldSubjectMod()

        self.v = MultipGameView(self.m)
        self.v.turn_on()

        self.c = MultiplayerGmCtrl()
        self.c.turn_on()
        self.c2 = PacketRecvCtrl(self.m)
        self.c2.turn_on()

        socketio_bridge.enable()

    def release(self):
        print('ClickChallg state released.')
        self.c.turn_off()
        self.c = None
        self.v.turn_off()
        self.v = None

        self.c2.turn_off()
        self.c2 = None

        socketio_bridge.disable()
