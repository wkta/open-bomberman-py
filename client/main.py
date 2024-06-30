import sys

# sys.path.append('../vendor')
import coremon_main
import glvars
from coremon_main.runners import StackBasedGameCtrl
from coremon_netw.NetwMsgCtrl import NetwMsgCtrl
from def_gamestates import GameStates
from glvars import SCR_SIZE, GAME_TITLE


if coremon_main.vernum not in('0.0.4', '0.0.5'):
    print('err! expected version of coremon>=0.0.4')
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
