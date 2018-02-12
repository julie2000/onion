#from scapy.all import scapy
import sys
import createSQL
import threading
from socket import *
from jump import onion

class server:
    def __init__(self):
        self.BUFSIZ = 1024
        self.HOST = self.get_ip_host()
        self.PORT = self.get_open_port()
        self.ADDR = (self.HOST, self.PORT)
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.flag = True
        self.sql = createSQL.sql()

    def get_ip_host(self):
        s = socket(AF_INET,SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print s.getsockname()[0]
        return s.getsockname()[0]

    def get_open_port(self):
        s = socket(AF_INET , SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        print port
        s.close()
        return port

    def open_sock(self):
        try: # try to connect
            self.serversock.bind(self.ADDR)
        except error as msg:
            print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            #sys.exit()
            flag = False  #?
        self.serversock.listen(2)  #in the project much more
        self.connection()

    def connection(self):
        print 'waiting for connection...'
        clientsock, addr = self.serversock.accept()
        print '...connected from:', addr
        t = onion(clientsock, addr, self.sql)
        try:
            threading.Thread(target=t.handler_tor, args=(addr,)).start()
            self.connection()
        except Exception:
            import traceback
            print traceback.format_exc()

    def terminate(self , s):
        s.close()