from PlayerAction import PlayerAction
from coremon_main import EventReceiver
from transversal.WorldSubjectMod import WorldSubjectMod
import glvars
from def_gevents import MyEvTypes
import socketio_bridge


class PacketRecvCtrl(EventReceiver):
    """
    handles all incoming network-related events
    """

    def __init__(self, given_mod: WorldSubjectMod):
        super().__init__()
        self._mod = given_mod
        self._last_sync = None

    def force_gs_sync(self):
        print('forcing sync...')
        for pl in glvars.allplayers:
            act_obj = PlayerAction(pl, PlayerAction.T_SYNCPOS)
            socketio_bridge.push_action(act_obj)  # provoque syncpos pour player pl

    def proc_event(self, ev, source):
        if ev.type == MyEvTypes.ConnectionOk:
            print('server login OK')
            print(ev.playercode)
            glvars.local_pl_code = ev.playercode
            glvars.allplayers.add(ev.playercode)
            socketio_bridge.join_room(glvars.local_pl_code, 1)
            self.force_gs_sync()

        elif ev.type == MyEvTypes.OtherGuyCame:
            glvars.allplayers.add(ev.plcode)
            self.force_gs_sync()

        elif ev.type == MyEvTypes.ServerStartingMatch:
            pass

        elif ev.type == MyEvTypes.BombCreation:
            self._mod.add_bomb(ev.x, ev.y)

        elif ev.type == MyEvTypes.BombExplosion:
            self._mod.remove_bomb(ev.x, ev.y)

        elif ev.type == MyEvTypes.PlayerMovement:  # MyEvTypes.GamestateServFeedback:
            self._mod.set_pos_from_netw(ev.plcode, ev.new_pos)
