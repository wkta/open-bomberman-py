from pygame.locals import USEREVENT


vernum = '0.0.4'

# -- constants
FIRST_ENGIN_TYPE = USEREVENT + 1
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
    return type('Enum', (), enums)


def enumeration_pr_events_engine(*sequential, **named):
    return enum_builder(True, FIRST_ENGIN_TYPE, *sequential, **named)


def enum_for_custom_event_types(*sequential, **named):
    return enum_builder(False, FIRST_CUSTO_TYPE, *sequential, **named)


EngineEvTypes = enumeration_pr_events_engine(
    'LogicUpdate',
    'Paint',
    'RefreshScreen',

    'PushState',  # contient un code state_ident
    'PopState',
    'ChangeState',  # contient un code state_ident

    'GameBegins',  # correspond à l'ancien InitializeEvent
    'GameEnds',  # indique que la sortie de jeu est certaine

    'AsyncRecv',  # [num] un N°identification & [msg] un string
    'AsyncSend',  # [num] un N°identification & [msg] un string
    
    'IngoingNetw',
    'OutgoingNetw'
)
