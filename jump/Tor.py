import socket as s
import sys
import thread
import server
import jump

class Tor:
    def __init__(self):
        self.s = server.server()
        self.s.who = True
        self.s.open_sock()
        #open proxy


Tor()