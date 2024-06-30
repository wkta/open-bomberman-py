from http.client import HTTPConnection

from coremon_main import EventReceiver, EngineEvTypes


class NetwMsgCtrl(EventReceiver):

    def __init__(self, port):
        super().__init__(True)  # sticky? Yeah

        self._numbuffer = -1
        self._buffer = None

        self.port = port

        self.host = None
        self.cli_http = None

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.OUTGOINGNETW:

            if (self.host is None) or self.host != ev.host:
                self.host = ev.host
                print('coremon_netw opening connection to {}:{}...'.format(self.host, self.port))
                self.cli_http = HTTPConnection(self.host, port=self.port)
                self.cli_http.connect()

            self._numbuffer = ev.num

            self._do_comm(ev.resource)

        elif ev.type == EngineEvTypes.GAMEENDS:
            if self.cli_http:
                print('coremon_netw closing connection...')
                self.cli_http.close()

    def _do_comm(self, resource):
        print('sending GET {} on {}'.format(resource, self.host))

        self.cli_http.request('GET', resource)
        resp = self.cli_http.getresponse()
        self._buffer = resp.read().decode()

        self.pev(EngineEvTypes.INGOINGNETW, msg=self._buffer, num=self._numbuffer)
        self._numbuffer = self._buffer = None

    @staticmethod
    def decompose(msg):
        """
        :param msg: could be "http://sc.gaudia-tech.com/yo.html", or "bidule.com/index.php:8100"
        :return: port, host, resource
        """
        # TODO autres cas que sc.gaudia-tech.com/yo.html
        print(msg)
        tmp_li = msg.split('/')
        print(tmp_li)
        host = tmp_li[0]
        resource = tmp_li[1]
        return None, host, resource
