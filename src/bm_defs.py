from coremon_main import enum_for_custom_event_types, CgmEvent
from coremon_main.util import enum_starting_from_zero


# gamestates
GameStates = enum_starting_from_zero(
    'MenuScreen',
    'ClickChallg'
)


# custom events
MyEvTypes = enum_for_custom_event_types(
    'PlSelectsMode',  # contains info: ev.k
    'WorldChanges',
    'ChallengeStarts',
)
CgmEvent.inject_custom_names(MyEvTypes)
