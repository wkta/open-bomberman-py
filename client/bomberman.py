import sys
sys.path.append('../vendor')

import coremon_main
import glvars
from def_gamestates import GameStates
from coremon_main.runners import StackBasedGameCtrl
from coremon_netw.NetwMsgCtrl import NetwMsgCtrl
from glvars import SCR_SIZE, GAME_TITLE


# 16h30
if coremon_main.vernum != '0.0.5':
    print('err! expected version of coremon>=0.0.5')
    sys.exit(1)


# - main program
coremon_main.init(SCR_SIZE, GAME_TITLE)

# controlers
ctrl = StackBasedGameCtrl(GameStates, GameStates.MenuScreen)
netctrl = NetwMsgCtrl(glvars.port)  # server runs on this port!

# activate controlers
ctrl.turn_on()
netctrl.turn_on()

# game
ctrl.loop()
coremon_main.cleanup()
print('done.')
