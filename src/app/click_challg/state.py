from coremon_main import BaseGameState, EventManager
from app.click_challg.view import ClickChallgView
from app.click_challg.ctrl import ClickChallgCtrl


class ClickChallgState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        print('entering ClickChallg state...')
        self.v= ClickChallgView()
        self.v.turn_on()
        self.c= ClickChallgCtrl()
        self.c.turn_on()

    def release(self):
        print('ClickChallg state released.')
        self.c.turn_off()
        self.c= None
        self.v.turn_off()
        self.v= None
