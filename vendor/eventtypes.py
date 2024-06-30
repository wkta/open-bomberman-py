from pygame.event import Event as PygameEvent
from pygame.event import post as pygame_event_post
from pygame import USEREVENT


# ---constants---##ffff00
from coremon_main import CgmEvent

__game = 220
__netw = 240
__timer = 21  # only < 32

NEWTURN      = __game  # playerid
ENDTURN      = __game+1  # playerid
SELECT       = __game+2  # playerid, landid
SELECTRESULT = __game+3  # landid, result 0=ok, 1=deselect, 2=notpossible (ai)
GSUPDATE     = __game+4  # None
ATTACKRESULT = __game+5  # aggressorid, defensorid, results
PLAYERDISCONN= __game+6  # playerid
PLAYERDEAD   = __game+7  # playerid
PLAYERWIN    = __game+8  # playerid
DROPDICE     = __game+9  # data ={land_id:num_dice}
STARTGAME    = __game+10  # None
ENDGAME      = __game+11  # playerid of winner
PLAYERRECONN = __game+12  # playerid

CONNINTERRUPT = __netw    # None
CONNECT       = __netw+1  # addr, port
DISCONNECT    = __netw+2  # addr, port
CHATMSG       = __netw+3  # msg

ELIZATIMER    = __timer   # None

MAGIC_CST = CgmEvent.ETYPE_ATTR_NAME  # important! doit être concordant avec la constante dans CgmEvent


# def post_new_turn(source, player_id):
#     """
#     Puts NEWTURN event on the pygame event queue.
#
#     Fields:
#     type    : NEWTURN
#     playerid: id of the player who start new turn.
#     """
#     pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: NEWTURN, "source":source, "playerid":player_id}))
#
#
# def post_end_turn(source, player_id):
#     """
#     Puts ENDTURN event on the pygame event queue.
#
#     Fields:
#     type    : ENDTURN
#     playerid: id of the player who ended turn
#     """
#     pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: ENDTURN, "source":source, "playerid":player_id}))


def post_select_land(source, player_id, land_id):
    """
    Puts SELECT event on the pygame event queue.
    
    Fields:
    type    : SELECT
    playerid: id of player
    landid  : id of the land which was selected
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: SELECT, "source":source, \
                                            "playerid":player_id, \
                                            "landid":land_id}))


def post_select_result(source, land_id, result):
    """
    Puts SELECTRESULT event on the pygame event queue.
    
    Fields:
    type    : SELECTRESULT
    landid  : id of the land which was selected
    ressult : 0=select, 1=deselect
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: SELECTRESULT, "source":source, \
                                                  "landid":land_id, \
                                                  "result":result}))


##def post_attack(source, aggressor_id, defensor_id):
##    """
##    Puts ATTACK event on the pygame event queue.
##    
##    Fields:
##    type        : ATTACK
##    aggressorid : land id which is attacking
##    defensorid  : land id which is defensing
##    """
##    pygame_event_post(pygame_event(ATTACK, {"source":source, \
##                                            "aggressorid":aggressor_id,\
##                                            "defensorid":defensor_id}))


def post_attack_result(source, aggresor_id, defensor_id, results):
    """
    Puts ATTACKRESULT event on the pygame event queue.
    
    Fields:
    type        : ATTACKRESULT
    aggressorid : land id which is attacking
    defensorid  : land id which is defensing
    results     : result of the attack -> ((dice pips, sum),(dice pips, sum))
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: ATTACKRESULT, "source":source, \
                                                  "aggressorid":aggresor_id,\
                                                  "defensorid":defensor_id,\
                                                  "results":results}))


def post_chatmsg(source, msg):
    """
    Puts a new chat message on the eventqueue.
    
    Fields:
    type : CHATMSG
    msg  : text
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: CHATMSG, "source":source, "msg":msg}))


def post_player_dead(source, player_id):
    """
    Puts an PLAYERDEAD event on the event queue
    
    Fields:
    type    : PLAYERDEAD
    playerid: id of the player which is dead
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: PLAYERDEAD, "source":source, \
                                                "playerid":player_id}))


def post_player_win(source, player_id):
    """
    Puts an PLAYERWIN event on the event queue
    
    Fields:
    type    : PLAYERWIN
    playerid: id of the player which is dead
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: PLAYERWIN, "source":source, \
                                               "playerid":player_id}))


def post_drop_dice(source, data):
    """
    Puts an DROPDICE event on the event queue.
    
    Fields:
    type : DROPDICE
    data : {landid: num_of_dices}
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: DROPDICE, "source":source, "data":data}))


def post_end_game(source):
    """
    Puts an ENDGAME event on the event queue.
    
    Fields:
    type: ENDGAME
    """
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: ENDGAME, "source":source}))


# def post_start_game(source):
#     """
#     Puts an STARTGAME event on the event queue.
#
#     Fields:
#     type: STARTGAME
#     """
#     pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: STARTGAME, "source":source}))


def post_gamestate_update(source, aggressor_id, defensor_id):
    """
    Puts ad GSUPDATE event on the event queue.
    
    Fields:
    type: GSUPDATE
    """
    print( "eventtypes: post game state update")
    pygame_event_post(PygameEvent(USEREVENT, {MAGIC_CST: GSUPDATE, "source":source, \
                                              "aggressorid":aggressor_id,
                                              "defensorid":defensor_id}))
