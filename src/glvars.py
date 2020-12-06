
# - constants
DEV_MODE = True

SCR_SIZE = (800, 600)
GAME_TITLE = 'Open Bomberman Py'

HOST_DEV = 'localhost'
PORT_DEV = 8100
HOST_PROD = 'wallet.gaudia-tech.com'
PORT_PROD = 80

# - global variables
host = HOST_PROD if DEV_MODE else HOST_DEV
