from coremon_main import EventReceiver, EngineEvTypes, EventManager, CgmEvent
from coremon_netw.EnvoiAsynchrone2 import EnvoiAsynchrone2
import defs_mco.glvars as glvars


class AsyncMessagingCtrl(EventReceiver):
    mem_timestamp = None

    def __init__(self):
        super().__init__(True)  # is sticky? YES

        # threads avec envoi / attente en cours
        self.set_of_threads = set()

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.ASYNCSEND:
            self.on_async_request(ev)
        elif ev.type == EngineEvTypes.LOGICUPDATE:
            self.on_logic_update(ev)
        # self.connect(EngineEvTypes.ASYNCCOMMAND, self.__proc_async_command)

    def on_async_request(self, ev):
        if EnvoiAsynchrone2.PORT is None:  # classe non initialisée
            EnvoiAsynchrone2.PORT = glvars.server_port
            EnvoiAsynchrone2.HOST_STR = glvars.server_host

        print('[AsyncMessagingCtrl] processing async request {}'.format(ev))
        id_req = ev.num
        msg_reseau = ev.msg

        thread = EnvoiAsynchrone2(id_req, msg_reseau, ev.data, self.__class__.mem_timestamp)

        # fonctionnement à éviter !
        # if ev.cb is not None:
        #    thread.setup_callback(ev.cb)

        self.set_of_threads.add(thread)
        thread.start()

    def on_logic_update(self, event):
        # aucun thread enregistré
        if len(self.set_of_threads) == 0:
            return

        # si tous les threads continuent leur exécution
        signes_activite = [not t.zombie_thread.isSet() for t in self.set_of_threads]
        if all(signes_activite):
            return

        # on sait que l'exécution d'au moins un thread s'est terminée
        new_set = set()
        for t in self.set_of_threads:
            if not t.zombie_thread.isSet():
                new_set.add(t)
                continue
            new_ev = CgmEvent(EngineEvTypes.ASYNCRECV, num=t.id_req, msg=t.response)
            EventManager.instance().post(new_ev)

        self.set_of_threads = new_set  # on "oublie" ainsi les threads zombie

    def __proc_async_command(self, ev):
        pass  # TODO utilité ?
        # app_const = AppConstants.instance()
        #
        # # if app_const.get_val('DEV_MODE'):  # désactivé sur serv de prod a cause dun gros bug comm réseau!!
        #
        #     #t = EnvoiAsynchrone(ev.hote, ev.ressource_http)
        #     # print('creation & lancement async worker avec msg: {}'.format(ev.ressource_http))
        # t = AsyncWorker(ev.id_commande, ev.ressource_http)
        # self.set_of_threads.add(t)
        # t.start()  # execute .run() sur le Thread en question, dans un fil d'exécution à part
