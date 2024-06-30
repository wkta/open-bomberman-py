import threading
from core.util.netw.PollingService import PollingService


class AsyncWorker(threading.Thread):
    NB_INST_MAX = 16
    nb_courant_instances = 0
    
    def __init__(self, id_commande, target_ressource):
        self.id_commande = id_commande
        self.target_ressource = target_ressource
        
        cls = self.__class__
        if cls.nb_courant_instances >= cls.NB_INST_MAX:
            raise Exception('Nb. maximum d\' appels asynchrones atteint')

        threading.Thread.__init__(self)
        self.setDaemon(True)
        
        cls.nb_courant_instances += 1

        self.zombie_thread = threading.Event() 
        self.response = None

        self.pservice = PollingService.instance()

    def __del__(self):
        self.__class__.nb_courant_instances -= 1

    def run(self):
        self.response = self.pservice.get_txt_data_via_http(self.target_ressource)
        self.zombie_thread.set()

    # DEPREC.  --- pour du test dummy uniquement
    # à l'époque on testait juste le long polling sur data.txt
    # def run_old(self):
    #     reponse_brute = f_long_polling_packet(self.test_timestamp)  # ancien
    #
    #     # traitement & mémorisation de la réponse
    #     b_inf = reponse_brute.index('{')
    #     b_sup = reponse_brute.index('}') + 1
    #     msg_json = reponse_brute[b_inf : b_sup]
    #
    #     dico_tmp = json.loads(msg_json)
    #     self.response = dico_tmp
    #
    #     self.zombie_thread.set()
