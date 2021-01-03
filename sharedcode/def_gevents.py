
SERV_COMM_KEY = 'coremon_evt_name'
PROD_SERVER_MODE = False

if not PROD_SERVER_MODE:
    from coremon_main import enum_for_custom_event_types, CgmEvent

else:
    FIRST_ENGIN_TYPE = 24 + 1  # pygame 2.0.0 has 24 constant as the pygame.locals.USEREVENT
    FIRST_CUSTO_TYPE = FIRST_ENGIN_TYPE + 20  # therefore, 20 is the maximal amount of engine events

    def enum_builder(to_upper, starting_index, *sequential, **named):
        domaine = range(starting_index, len(sequential) + starting_index)
        enums = dict(zip(sequential, domaine), **named)
        tmp_inv_map = {v: k for k, v in enums.items()}
        tmp_all_codes = domaine

        if to_upper:
            tmp = dict()
            for k, v in enums.items():
                if k == 'inv_map' or k == 'all_codes':
                    continue
                tmp[k.upper()] = v
            enums = tmp

        enums['inv_map'] = tmp_inv_map
        enums['all_codes'] = tmp_all_codes
        enums['last_code'] = len(sequential) + starting_index - 1
        return type('Enum', (), enums)

    def enum_for_custom_event_types(*sequential, **named):
        return enum_builder(False, FIRST_CUSTO_TYPE, *sequential, **named)


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
    'ChallengeEnds',  # someone just won => the game ends

    # - INGAME network-related
    'OtherGuyCame',  # contains gamestate
    'PlayerMovement',  # contains>> plcode:int, new_pos:list
    'BombCreation',  # contains>> author:int, genesis_t:float, x:int, y:int
    'BombExplosion',  # contains>> x:int, y:int
)

if not PROD_SERVER_MODE:
    CgmEvent.inject_custom_names(MyEvTypes)
