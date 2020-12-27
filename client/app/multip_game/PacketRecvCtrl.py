import time

import glvars
import socketio_bridge
from WorldModel import WorldModel
from coremon_main import EventReceiver, EngineEvTypes
from def_gevents import MyEvTypes
from transversal.WorldSubjectMod import WorldSubjectMod


class PacketRecvCtrl(EventReceiver):
    """
    handles all incoming network-related events
    """

    def __init__(self, given_mod: WorldSubjectMod):
        super().__init__()
        self._mod = given_mod
        self._last_sync = None

        # for a super basic countdown...
        self._debug_countdown = None
        self.numtoprint = -1

    # def force_gs_sync(self):
    #     print('forcing sync...')
    #     for pl in glvars.allplayers:
    #         act_obj = PlayerAction(pl, PlayerAction.T_SYNCPOS)
    #         socketio_bridge.push_action(act_obj)  # provoque syncpos pour player pl

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:

            if self._debug_countdown is not None:
                if ev.curr_t - self._debug_countdown > 1:
                    print(self.numtoprint)
                    self._debug_countdown += 1
                    self.numtoprint -= 1

                if self.numtoprint < 0:
                    self._debug_countdown = None

        elif ev.type == MyEvTypes.ConnectionOk:
            print('server login OK')
            print(ev.playercode)
            glvars.local_pl_code = ev.playercode
            glvars.allplayers.add(ev.playercode)
            socketio_bridge.join_room(glvars.local_pl_code, 1)
            # self.force_gs_sync()

        elif ev.type == MyEvTypes.OtherGuyCame:
            tmp = WorldModel.deserialize(ev.gamestate)
            self._mod.irepr.sync_state(tmp)
            self._mod.tag_gs_change()

            if len(self._mod.irepr.list_players()) >= 2:
                self._debug_countdown = time.time()
                self.numtoprint = WorldModel.COUNTDOWN_DUR

        elif ev.type in (MyEvTypes.BombCreation, MyEvTypes.BombExplosion):
            tmp = WorldModel.deserialize(ev.gamestate)
            self._mod.irepr.sync_state(tmp)
            self._mod.tag_gs_change()

        elif ev.type == MyEvTypes.ChallengeStarts:
            tmp = WorldModel.deserialize(ev.gamestate)
            self._mod.irepr.sync_state(tmp)

        elif ev.type == MyEvTypes.ChallengeEnds:
            tmp = WorldModel.deserialize(ev.gamestate)
            print(' *** match winner is : {} *** '.format(tmp.match_winner))
            self.pev(EngineEvTypes.POPSTATE)

        elif ev.type == MyEvTypes.PlayerMovement:  # MyEvTypes.GamestateServFeedback:
            tmp = WorldModel.deserialize(ev.gamestate)
            self._mod.irepr.sync_state(tmp)
            self._mod.tag_gs_change()
