
# - constants
DEV_MODE = True
NEED_NETW_DEBUG = False

SCR_SIZE = (1024, 860)
CELL_SIZE_PX = 64
GAME_TITLE = 'Open Bomberman Py'

HOST_DEV = 'localhost'
PORT_DEV = 8577

HOST_PROD = 'wallet.gaudia-tech.com'
PORT_PROD = 80

# - global variables
# TODO: instead of player codes, let us use usernames + room management
local_pl_code = None
allplayers = set()

host = HOST_PROD if (not DEV_MODE) else HOST_DEV
port = PORT_PROD if (not DEV_MODE) else PORT_DEV
