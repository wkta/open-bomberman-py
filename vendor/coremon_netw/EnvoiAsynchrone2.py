import threading
import urllib.parse as pp
from http.client import HTTPConnection

from HttpServer import HttpServer


class EnvoiAsynchrone2(threading.Thread):
    NB_INST_MAX = 16
    nb_courant_instances = 0

    PORT = None
    HOST_STR = None
    
    def __init__(self, id_req, http_ressource, opt_data, test_timestamp=None):
        cls = self.__class__
        if cls.nb_courant_instances >= cls.NB_INST_MAX:
            raise Exception('Nb. maximum d\' appels asynchrones atteint')

        self.id_req = id_req

        self.test_timestamp = '1523728737' if (test_timestamp is None) else test_timestamp
        threading.Thread.__init__(self)
        cls.nb_courant_instances += 1

        self.post_data = opt_data  # peut être None si on fait du get, ou set correctement pour du POST

        # - TEMPORAIRE
        self.server_port = self.__class__.PORT
        self.host = self.__class__.HOST_STR

        self.url_pr_server_time = None
        self.debug_mode = None
        
        self.target_http_ressource = http_ressource  # TODO utiliser vraiment la commande recue !
        self.zombie_thread = threading.Event() 
        self.response = None
        self.cb = None

    def setup_callback(self, cb):
        self.cb = cb

    def __del__(self):
        self.__class__.nb_courant_instances -= 1

    def stop(self):
        self.cli_http.close()

    def f_long_polling_packet(self, ts_arg):
        if self.server_port is None:  # si non initialisé
            self.server_port = 80
            self.host = '192.168.1.99'
            self.url_pr_server_time = '/tom/server.php'
            self.debug_mode = True

            #self.cli_http = HTTPConnection(self.host)
            #self.cli_http.connect()

        # transmission
        msg = self.url_pr_server_time + '?timestamp={}'.format(ts_arg)

        res = EnvoiAsynchrone2._commit_to_netw(self.host, msg)
        return res

    @staticmethod
    def send_get_request(host, url):
        assert host is not None
        assert isinstance(url, str)

        print()
        print('---DEBUG NETW.---')
        print('method GET')
        print(str(host))
        print(str(url))
        print('...')

        cli_http = HTTPConnection(host)
        cli_http.connect()
        cli_http.request('GET', url)
        resp = cli_http.getresponse()
        txt = resp.readall().decode('ascii')
        print(txt)
        print('-----------------')
        return txt

    @staticmethod
    def send_post_request(host, url, post_data_dict):

        print()
        print('---DEBUG NETW.---')
        print('method POST')
        print(str(host))
        print(str(url))
        print(str(post_data_dict))
        print('...')

        params = pp.urlencode(post_data_dict)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

        cli_http = HTTPConnection(host)
        cli_http.connect()
        cli_http.request('POST', url, params, headers)
        resp = cli_http.getresponse()
        txt = resp.readall().decode('ascii')
        print(txt)
        print('-----------------')
        return txt

    def run(self):
        url = 'http://{}/{}'.format(self.host, self.target_http_ressource)
        if self.post_data is not None:
            #self.response = EnvoiAsynchrone2.send_post_request(self.host, url, {'data': self.post_data})
            self.response = HttpServer.instance().proxied_post(url, {'data': self.post_data})
        else:
            #self.response = EnvoiAsynchrone2.send_get_request(self.host, url)
            self.response = HttpServer.instance().proxied_get(url, {})  #, {'data': self.post_data})

        self.zombie_thread.set()  # on indique que la tâche du thread est terminée

        # obj = json.loads(reponse_brute)
        # # traitement & mémorisation de la réponse
        # b_inf = reponse_brute.index('{')
        # b_sup = reponse_brute.index('}') + 1
        # msg_json = reponse_brute[b_inf:b_sup]
        # dico_tmp = json.loads(msg_json)
        # dico_tmp['data_from_file'] = dico_tmp['data_from_file'].rstrip("\n")
