#!/usr/bin/env python
import time
import sys
import MySQLdb

class MySQL:
    _conn = None

    def __init__(self,host,user,password,database,charset = 'utf8',port = 3306,socket = None):
        self.host = host
        self.user = user
        self.passwd = password
        self.port = port
        self.socket = socket
        self.db = database
        self.charset = charset

    def reconnect(self):
        """Basic MySQL connection functionality"""
        self._conn = None

        while self._conn is None:
            try:
                if not self.socket:
                    self._conn = MySQLdb.connect(
                        user = self.user,
                        passwd = self.passwd,
                        port = self.port,
                        host = self.host,
                        db = self.db,
                        charset = self.charset,
                        init_command = "SET SESSION wait_timeout=100"
                    )
                else:
                    self._conn = MySQLdb.connect(
                        user = self.user,
                        passwd = self.passwd,
                        host = self.host,
                        unix_socket = self.socket,
                        init_command = "SET SESSION wait_timeout=100"
                    )

            except MemoryError:
                print sys.exc_info()
                sys.exit(1)
            except MySQLdb.Error:
                print sys.exc_info()
                time.sleep(1)

    def basequery(self,query,fetch_type = 0):
        """
        fetch_type:
        fetch_row([maxrows, how]) -- Fetches up to maxrows as a tuple.
        The rows are formatted according to how:
            0 -- tuples (default)
            1 -- dictionaries, key=column or table.column if duplicated
            2 -- dictionaries, key=table.column
        """

        # Establish connection if not existing or fails to ping
        if not self._conn:
            self.reconnect()
        print fetch_type
        # We will retry just once - reconnect has infinite loop though
        try:
            for attempt in (True,False):
                try:
                    self._cur = self._conn.cursor()
                    if fetch_type:
                        self._cur._fetch_type = fetch_type
                    self._cur.execute(query)
                    break  # if successful
                except MySQLdb.OperationalError:
                    if attempt:
                        self.reconnect()
                        continue
                    else:
                        return None

        except MySQLdb.Error,e:
            print 'ok'
            print e
            return None

        return True

    def qone(self,query,fetch_type = 0):
        ret = None
        if self.basequery(query,fetch_type):
            ret = self._cur.fetchone()
            self.close()
        return ret

    def qmany(self,query,fetch_type = 0):
        ret = None
        if self.basequery(query,fetch_type):
            ret = self._cur.fetchall()
        self.close()
        return ret

    def qdml(self,query):
        if self.basequery(query):
            self._conn.commit()
        else:
            self._conn.rollback()
        self.close()

    def close(self):
        self._cur.close()
        self._conn.close()


if __name__ == "__main__":
    #print MySQL('172.20.150.3','huang','huang123','valentine0606').qone("select * from ms_user limit 1",0)
    #conn =  MySQL('172.20.150.3','huang','huang123','test')
    #id = 5
    #name = "aa"
    #sql = "insert into t1 values(%d,'%s')"%(id,name)
    #print sql
    #conn.qdml(sql)
    pass
