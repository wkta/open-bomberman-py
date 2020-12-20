import random

from WorldModel import WorldModel


# - variables
world = WorldModel()
prev_plcodes = dict()
pl_to_room = dict()
force_quit = False


def fetch_room(plname):
    global pl_to_room
    if plname in pl_to_room:
        return pl_to_room[plname]


def gen_username():
    global prev_plcodes
    num = random.randint(998, 2866791137)
    while num in prev_plcodes:
        num = random.randint(998, 2866791137)
    return num


def save_room(plname, room):
    global pl_to_room
    if room is None:
        del pl_to_room[plname]
    else:
        pl_to_room[plname] = room


# ----------------------------
#  INGAME STUFF
# ----------------------------
def bomb_delay():
    return WorldModel.BOMB_DELAY


def locate_player(plcode):
    global world
    return world.player_location(plcode)


def maj_gamestate(plcode: int, direct: int):
    global world

    print(' SERV: maj gamestate')

    tmp = world.player_location(plcode)
    if direct == 0:
        tmp[0] += 1
        if tmp[0] >= WorldModel.GRID_SIZE:
            tmp[0] = WorldModel.GRID_SIZE-1

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
        if tmp[1] >= WorldModel.GRID_SIZE:
            tmp[1] = WorldModel.GRID_SIZE-1

    world.change_pl_position(plcode, tmp)


def spawn_player(plcode):
    global world
    return world.consume_spawn(plcode)


# def loadstate():
#     global gamestate
#     gmstate = gamestate
#     with open('gamestate.json', 'r') as fptr:
#         obj = json.load(fptr)
#
#         gmstate.clear()
#         for k, v in obj.items():
#             gmstate[int(k)] = v
#         return True
