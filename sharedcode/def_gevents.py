from coremon_main import enum_for_custom_event_types, CgmEvent


SERV_COMM_KEY = 'coremon_evt_name'


MyEvTypes = enum_for_custom_event_types(

    'PlSelectsMode',  # contains info: ev.k
    'GamestateServFeedback',  # used for sync client game state! Contains: plcode, new_pos
    'PlayerMoves',  # updating only view from player moves! Contains: plcode, new_pos

    # - model-to-view comm.
    'BombsetChanges',  # contains>> info:set of bomb locations

    # - network-related
    'ConnectionOk',  # contains>> playercode:int
    'ServerStartingMatch',  # the server automatically starts a new match after 10sec
    'ChallengeStarts',

    # - INGAME network-related
    'OtherGuyCame',  # contains plcode, initpos
    'PlayerMovement',  # contains>> plcode:int, new_pos:list
    'BombCreation',  # contains>> author:int, genesis_t:float, x:int, y:int
    'BombExplosion',  # contains>> x:int, y:int
)
CgmEvent.inject_custom_names(MyEvTypes)
