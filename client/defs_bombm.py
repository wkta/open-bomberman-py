from coremon_main import enum_for_custom_event_types, CgmEvent
from coremon_main.util import enum_starting_from_zero


# gamestates
GameStates = enum_starting_from_zero(
    'MenuScreen',
    'MultipGame'
)


# custom events
MyEvTypes = enum_for_custom_event_types(
    'ServerLoginOk',  # contains username
    'OtherGuyCame',  # contains username

    'ServerStartingMatch',  # the server automatically starts a new match after 10sec

    'PlSelectsMode',  # contains info: ev.k

    'GamestateServFeedback',  # used for sync client game state! Contains: plcode, new_pos
    'PlayerMoves',  # updating only view from player moves! Contains: plcode, new_pos

    'ChallengeStarts',
)
CgmEvent.inject_custom_names(MyEvTypes)
