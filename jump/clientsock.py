from socket import *
import thread
import sys
import os

class clientsock(object):
    """
    An echo client communication.
    Methods:
        constructor(): get destination IP (server) and open a TCP socket
        get_dst_port(): gets the destination port, checks if the input is valid
        connect(): starting communication with server
        rcv(): receives a message from server and checks if port has been changed. If yes, the communication will be restarted.
        snd(): sends a message to server.
        quit(): ends communication amd closes socket.
    Attributes:
        BUFSIZ: max size of a message
        dst_ip = server's IP address
        dst_port: server's port
        sock: the socket we use for communication
    """

    def __init__(self, ip , port):
        self.BUFSIZ = 1024
        self.dst_ip = str(ip)
        self.dst_port =  int(port)
        self.sock = socket(AF_INET, SOCK_STREAM)
        print "init"

    def connect(self):
        server_address = (self.dst_ip, self.dst_port)
        print 'connecting to %s port %s' % server_address
        print "con 1"
        self.sock.connect(server_address)


    def rcv(self):
        return self.sock.recv(self.BUFSIZ)

    def snd(self, message):
        self.sock.send(message)

    def quit(self):
        self.sock.close()


