from socket import *
import thread
import sys
import os
import time


class clientsock(object):

    def __init__(self, ip, port):
        self.BUFSIZ = 1024
        self.HOST = self.get_ip_host()  # of tiny server
        self.PORT = self.get_open_port()# of tiny server
        self.ADDR = (self.HOST, self.PORT)# of tiny server
        self.dst_ip = ip # tor server
        self.dst_port = port# tor server
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.serversock.bind(self.ADDR)
        self.serversock.listen(1)
        self.ip_hop = None  #go to node
        self.port_hop = None#go to node

    def connecti(self):
        server_address = (self.dst_ip, self.dst_port)  #tor
        print 'connecting to %s port %s' % server_address
        self.sock.connect(server_address)
        self.sock.send(str(self.PORT))
        self.sock.recv(self.BUFSIZ)
        #time.sleep(5)
        self.quit()
        thread.start_new_thread(self.handler, ())

    def get_ip_host(self):
        s = socket(AF_INET, SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print s.getsockname()[0]
        return s.getsockname()[0]

    def get_open_port(self):
        s = socket(AF_INET, SOCK_STREAM)
        s.bind(("", 0))
        s.listen(1)
        port = s.getsockname()[1]
        print port
        s.close()
        return port

    def rcv(self):
        return self.sock.recv(self.BUFSIZ)

    def snd(self, message, dst): #?
        sock = socket(AF_INET, SOCK_STREAM)
        server_address = (self.dst_ip, self.dst_port)
        sock.connect(server_address)
        #sock.send(".")
        #time.sleep(5)
        sock.send(dst)
        sock.recv(1024)
        sock.send(message)
        sock.recv(1024)
        sock.close()

    def handler(self):
        #try: # try to connect
        #    self.serversock.bind(self.ADDR)
        #except error as msg:
        #    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            #sys.exit()
        #self.serversock.listen(1)
        self.connection()

    def connection(self):
        clientsock, addr = self.serversock.accept()
        #print '...connected from:', addr
        thread.start_new_thread(self.jumping, (clientsock, addr))
        self.connection()

    def jumping(self,clientsock,addr):

        if addr[0] == self.dst_ip : ##server
            if self.ip_hop:
                data = clientsock.recv(self.BUFSIZ)
                clientsock.close()
                print "yayy"
                ADDR = (self.ip_hop, int(self.port_hop))
                s = socket(AF_INET, SOCK_STREAM)
                s.connect(ADDR)
                s.send(data)
                time.sleep(2)
                s.close()
                self.ip_hop = None
            else:
                self.ip_hop = clientsock.recv(self.BUFSIZ)
                self.port_hop = clientsock.recv(self.BUFSIZ)
                place = clientsock.recv(self.BUFSIZ)
                #if place == 1:
                 #   data = clientsock.recv(self.BUFSIZ)
                  #  clientsock.close()
                   # ADDR = (self.ip_hop,self.port_hop)
                 #   s = socket(AF_INET, SOCK_STREAM)
                  #  s.connect(ADDR)
                   # s.send(data)
                 #   sys.sleep(2)
                  #  s.close()
                   # self.ip_hop = None
                #else:
                clientsock.close()
            print "ok"
        else:
            print "nope"
            print clientsock.recv(self.BUFSIZ)
            clientsock.close()


    def quit(self):
        self.sock.close()



