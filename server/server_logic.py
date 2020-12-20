import json
import random

from WorldModel import WorldModel


# - const
BOMB_DELAY = 2.97  # sec
BSUP = 8


# - variables
prev_plcodes = dict()
pl_to_room = dict()
bombs = dict()  # assoc position time it was planted
gamestate = dict()
force_quit = False


def spawn_player(plcode):
    global gamestate
    gamestate[plcode] = [0, 1]


def user_to_code(uname):
    return int(uname[uname.find('0x') + 2:], 16)


def save_room(plname, room):
    global pl_to_room
    if room is None:
        del pl_to_room[plname]
    else:
        pl_to_room[plname] = room


def locate_player(plcode):
    global gamestate
    return gamestate[plcode]


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


def loadstate():
    global gamestate
    gmstate = gamestate
    with open('gamestate.json', 'r') as fptr:
        obj = json.load(fptr)

        gmstate.clear()
        for k, v in obj.items():
            gmstate[int(k)] = v
        return True


def maj_gamestate(plcode: int, direct: int):
    global gamestate

    print(' SERV: maj gamestate')
    k = int(plcode)
    d = int(direct)
    if d == 0:
        gamestate[k][0] += 1
        if gamestate[k][0] >= WorldModel.GRID_SIZE:
            gamestate[k][0] = WorldModel.GRID_SIZE-1

    elif d == 1:
        gamestate[k][1] -= 1
        if gamestate[k][1] < 0:
            gamestate[k][1] = 0

    elif d == 2:
        gamestate[k][0] -= 1
        if gamestate[k][0] < 0:
            gamestate[k][0] = 0

    elif d == 3:
        gamestate[k][1] += 1
        if gamestate[k][1] >= WorldModel.GRID_SIZE:
            gamestate[k][1] = WorldModel.GRID_SIZE-1
