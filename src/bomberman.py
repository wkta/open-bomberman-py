import coremon_main
from bm_defs import GameStates
from coremon_main.runners import StackBasedGameCtrl
from glvars import SCR_SIZE, GAME_TITLE


# 16h30

print(coremon_main.vernum)

# - main program
coremon_main.init(
    SCR_SIZE,
    GAME_TITLE
)
ctrl = StackBasedGameCtrl(GameStates, GameStates.MenuScreen)

# - run the game
ctrl.turn_on()
ctrl.loop()

coremon_main.cleanup()
print('done.')
