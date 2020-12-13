
# - constants
DEV_MODE = False

SCR_SIZE = (800, 600)
GAME_TITLE = 'Open Bomberman Py'

HOST_DEV = 'localhost'
PORT_DEV = 8577

HOST_PROD = 'wallet.gaudia-tech.com'
PORT_PROD = 80

# - global variables
local_pl_code = 1
allplayers = {1, 2}

host = HOST_PROD if (not DEV_MODE) else HOST_DEV
port = PORT_PROD if (not DEV_MODE) else PORT_DEV
