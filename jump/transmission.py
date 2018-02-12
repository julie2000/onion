from scapy.all import scapy
import sys
import thread
import random

class transmissin:
    def __init__(self, ip, sql):
        self.ip_dst = ip
        self.sql = sql
        self.ip_row = self.sql.get_row(ip)
        self.max = 3


