import random

from WorldModel import WorldModel


# - variables
world = WorldModel()
world.load_level('gamelevel.json')

prev_plcodes = dict()
pl_to_room = dict()
force_quit = False


def fetch_room(plname):
    global pl_to_room
    if plname in pl_to_room:
        return pl_to_room[plname]


def gen_username():
    global prev_plcodes
    num = random.randint(1000, 1999)
    while num in prev_plcodes:
        num = random.randint(1000, 1999)
    return num


def save_room(plname, room):
    global pl_to_room
    if room is None:
        del pl_to_room[plname]
    else:
        pl_to_room[plname] = room


# ----------------------------
#  IN-GAME STUFF
# ----------------------------
def maj_gamestate(plcode: int, direct: int):
    """
    attempts to perform player movement.

    :param plcode:
    :param direct: 0, 1, 2, 3 counter-clockwise direction code, starts at East direction, then North etc.

    :return: True if gamestate has changed... False otherwise
    """
    global world

    tmp = world.player_location(plcode)
    if direct == 0:
        tmp[0] += 1
        if tmp[0] >= WorldModel.GRID_WIDTH:
            tmp[0] = WorldModel.GRID_WIDTH-1

    elif direct == 1:
        tmp[1] -= 1
        if tmp[1] < 0:
            tmp[1] = 0

    elif direct == 2:
        tmp[0] -= 1
        if tmp[0] < 0:
            tmp[0] = 0

    elif direct == 3:
        tmp[1] += 1
        if tmp[1] >= WorldModel.GRID_HEIGHT:
            tmp[1] = WorldModel.GRID_HEIGHT-1

    if world.can_walk(tmp):
        world.change_pl_position(plcode, tuple(tmp))
        return True

    return False
