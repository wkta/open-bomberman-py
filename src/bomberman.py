import coremon_main
from bm_defs import GameStates
from coremon_main.runners import StackBasedGameCtrl
from coremon_netw.NetwMsgCtrl import NetwMsgCtrl
from glvars import SCR_SIZE, GAME_TITLE
import sys

# 16h30

if coremon_main.vernum != '0.0.4':
    print('err! expected version of coremon==0.0.4')
    sys.exit(1)

# - main program
coremon_main.init(
    SCR_SIZE,
    GAME_TITLE
)
ctrl = StackBasedGameCtrl(GameStates, GameStates.MenuScreen)

# handling netw.
netctrl = NetwMsgCtrl()  # server runs on this port!
netctrl.turn_on()

# - run the game
ctrl.turn_on()
ctrl.loop()

coremon_main.cleanup()
print('done.')
