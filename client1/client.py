from socket import *
import thread
import sys
import os
import clientsock

class tor_client():
    def __init__(self):
        self.sclient  = clientsock.clientsock('172.16.13.132',2816)
        self.sclient.connecti()
        self.snd_message()

    def snd_message(self):
        data = raw_input("would you like to send something?")
        ip_dst = raw_input("who to?")
        self.sclient.snd(data, ip_dst)
        self.snd_message()

tor_client()

#172.17.21.14