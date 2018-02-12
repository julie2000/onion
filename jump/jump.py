#from scapy.all import *
import socket as s
import sys
import thread
import server
import createSQL
import threading
import random
import clientsock
import time

class onion:
    def __init__(self, client, addr, sql):
        self.main_cli = client
        self.ip_dst = addr[0]
        print self.ip_dst
        self.cli_port = client.getsockname()[1]
        self.sql = sql
        self.ip_row = 0
        self.max = 3
        self.event = threading.Event()
        self.event.set()
        self.ip_hops = []
        self.port_hops = []
        self.dst_hop = None
        self.data = None


    def handler_tor(self, addr ):
        try:
            self.main_cli.settimeout(10)
            print "startng"
            a = self.main_cli.recv(1024)
            print a
            self.dst_hop  = a
            self.put_in_sql(self.main_cli, addr,self.dst_hop)  # if not exists
            self.main_cli.send("got it")
            print "hi", self.dst_hop
            try:
                self.data = self.main_cli.recv(1024)
                if self.data:
                    self.main_cli.send("got it")
                    self.main_cli.close()
                    print "mop", self.data
                    self.ip_row = self.sql.get_row(self.dst_hop)[0]
                    print self.ip_row , "row"
                    self.select_ip()  ###
                else:
                    self.main_cli.close()
            #self.main_cli.send("got it")
            except Exception:
                import traceback
                print traceback.format_exc()
                print "mip"

                #self.main_cli.terminate(self.main_cli)

                self.main_cli.close()



        except Exception:
            import traceback
            print traceback.format_exc()


    def select_ip(self):
        if self.max > self.sql.row:
            self.max = self.sql.row
        #if self.ip_row is None:
           # self.ip_row = -1
        row_num = []

        for i in range(3):
            #if i+1 != self.ip_row:
            row_num.append( i+1)

        for i in range(3):
            self.find_ip(row_num,i )

        self.send_hops()

        jump_serv = clientsock.clientsock(self.ip_hops[0], int(self.port_hops[0]) ) #####
        jump_serv.connect()
        jump_serv.snd(self.data)
        jump_serv.quit()

        print "done"

    def find_ip(self,row_num, i ):
        rnd_row = random.choice(row_num)
        self.check_if_ava(self.sql.get_ip(rnd_row),row_num,rnd_row)


    def check_if_ava(self , ip, row_num , rnd_row): #icmp
        #packet = IP(dst=ip)/ICMP()
        #reply = sr1(packet, timeout=5)
        #if reply is None:
         #   self.sql.remove_ip(ip)
         #   row_num.remove(row_num)
         #   self.find_ip(row_num,i)
        #else:
        if ip == self.dst_hop or self.ip_dst == ip:
            print "remove"
            row_num.remove( rnd_row)
        else:
            self.ip_hops.append(ip)
            self.port_hops.append(self.sql.get_port(rnd_row))
            row_num.remove( rnd_row)

    def send_hops(self):
        for i in range(len(self.ip_hops)-1):
            if len(self.ip_hops) <=1:
                print "working"
                pass
            else:
                print "else"
                jump_serv = clientsock.clientsock(self.ip_hops[i], int(self.port_hops[i])) #####
                jump_serv.connect()
                jump_serv.snd(self.ip_hops[i])
                time.sleep(5)
                jump_serv.snd(str(self.port_hops[i]))
                time.sleep(5)
                jump_serv.snd(str(i+1))
                jump_serv.quit()

        jump_serv = clientsock.clientsock(self.ip_hops[-1], self.port_hops[-1])  #####
        jump_serv.connect()
        jump_serv.snd(self.dst_hop)
        time.sleep(5)
        jump_serv.snd(str(self.sql.get_port(self.ip_row)))
        time.sleep(5)
        jump_serv.snd(str(len(self.ip_hops)))
        jump_serv.quit()

    def put_in_sql(self,clientsock, addr, port):
        self.event.wait()
        self.event.clear()
        self.sql.insert_ip(clientsock, addr, port)
        self.event.set()