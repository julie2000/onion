import sqlite3
from socket import *

class sql:
    def __init__(self):
        try:
            self.db = sqlite3.connect('ip_table')
            cursor = self.db.cursor()
            # Check if table users does not exist and create it
            cursor.execute('''CREATE TABLE IF NOT EXISTS
                          clients(row INTEGER PRIMARY KEY unique, origin_ip TEXT unique, new_ip TEXT , port INTEGER)''')

            #print cursor.execute("SHOW CREATE TABLE clients")
            # Commit the change
            self.db.commit()
            self.row = self.find_rows()
        except Exception as e:
            # Roll back any change if something goes wrong
           # self.db.rollback()
            raise e
        #finally:
            #self.db.close()

    def insert_ip(self,sock, addr , porti): #at the moment insert only old ip and mac

        print self.row
        self.row = self.row +1
        try:
            self.db = sqlite3.connect('ip_table')
            cursor = self.db.cursor()
            cursor.execute('''INSERT INTO clients(row, origin_ip, new_ip, port)
                      VALUES(?,?,?,?)''', (self.row, str(addr[0]), ".", porti)) #change new ip
            self.db.commit()

        except Exception as e:
              # Roll back any change if something goes wrong
            self.db.rollback()
            #raise e

    def find_rows(self):
         try:
            self.db = sqlite3.connect('ip_table')
            cursor = self.db.cursor()
            cursor.execute('''SELECT max(row) FROM clients ''')
            if cursor.fetchone()[0]:
                return cursor.fetchone()[0]
            return 0
         except Exception as e:
              # Roll back any change if something goes wrong
            self.db.rollback()
            return 0

    def get_ip(self,row):
        try:
            self.db = sqlite3.connect('ip_table')
            cursor = self.db.cursor()
            cursor.execute('''SELECT origin_ip FROM clients WHERE row=?''', (row,)) #change to new
            return cursor.fetchone()[0]
        except Exception as e:
            raise e


    def get_port(self, row):
        try:
            self.db = sqlite3.connect('ip_table')
            cursor = self.db.cursor()
            cursor.execute('''SELECT port FROM clients WHERE row=?''', (row,))  # change to new
            return cursor.fetchone()[0]
        except Exception as e:
            raise e

    def remove_ip(self, addr):
        try:
            self.db = sqlite3.connect('ip_table')
            cursor = self.db.cursor()
            cursor.execute('''SELECT row FROM clients WHERE origin_ip=?''', (addr,))
            row_removed = cursor.fetchone()[0]
            cursor.execute('''DELETE FROM clients WHERE row = ? ''', (row_removed,))
            for i in range(0,self.row - row_removed):
                cursor.execute('''UPDATE clients SET row = ? WHERE row = ? ''',
                    (row_removed - i, row_removed))
            self.db.commit()
            self.row -=1
        except Exception as e:
              # Roll back any change if something goes wrong
            self.db.rollback()
            raise e

    def update(self):  #if crush and port change...
        pass

    def get_row(self, ip_dst):
        self.db = sqlite3.connect('ip_table')
        cursor = self.db.cursor()
        cursor.execute('''SELECT row FROM clients WHERE origin_ip=?''', (ip_dst,))
        row_ip = cursor.fetchone()
        return row_ip


#db = sqlite3.connect('ip_tables')
#cursor = db.cursor()
#cursor.execute("DROP TABLE clients")
#print "yay"

