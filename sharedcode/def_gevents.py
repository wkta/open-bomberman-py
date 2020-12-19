from coremon_main import enum_for_custom_event_types, CgmEvent


SERV_COMM_KEY = 'coremon_evt_name'


MyEvTypes = enum_for_custom_event_types(
    'OtherGuyCame',  # contains username

    'ServerStartingMatch',  # the server automatically starts a new match after 10sec

    'PlSelectsMode',  # contains info: ev.k

    'GamestateServFeedback',  # used for sync client game state! Contains: plcode, new_pos
    'PlayerMoves',  # updating only view from player moves! Contains: plcode, new_pos

    # - network-related
    'ConnectionOk',  # contains playercode:int
    'PlayerMovement',  # contains plcode:int, new_pos:list

    'ChallengeStarts',
)
CgmEvent.inject_custom_names(MyEvTypes)
