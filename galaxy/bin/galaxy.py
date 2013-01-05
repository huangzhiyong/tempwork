#!/usr/bin/env python
# - * - coding: utf-8 -*-
#import threading
import sys,json
#import traceback
import socket
from SocketServer import TCPServer as TCP,StreamRequestHandler as SRH,ThreadingMixIn as TMI
from galaxy.bin.globaldef import config,blog
from galaxy.bin.daemon import Daemon
from galaxy.bin.mysql import MySQL
from galaxy.bin.ping import *

import time

class Ping(object):
    def __init__(self):
        self.p_timeout = 2
        self.s_timeout = 5
        self.status_list = [1 for i in range(0,10)]


    def pingCheck(self,dest_addr,port):
        """
        ping host,check host is alive and port is open
        """
        for i in range(0,10):
            blog.info("ping %s with ..." % dest_addr)
            try:
                delay = do_one(dest_addr,self.p_timeout,64)
            except Exception,err:
                blog.error("Network error...%s" % (str(err)))
                return False
            if delay is None:
                self.status_list.insert(0,0)
                self.status_list.pop()
                blog.error("Failed.(timeout within %ssec)" % self.p_timeout)
            else:
                #delay = delay * 1000
                self.status_list.insert(0,1)
                self.status_list.pop()
                #blog.info("get ping in %0.4fms"%(delay))
                time.sleep(1)

        if  5 <= self.status_list.count(1) <= 10:
            sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            sk.settimeout(self.s_timeout)
            try:
                sk.connect((dest_addr,int(port)))
                blog.info("%s status to Up,port %s is Up" % (dest_addr,port))
            except Exception:
                blog.error("%s status to Up,port %s is Down" % (dest_addr,port))
                sk.close()
                return False
            sk.close()
            return True
        else:
            blog.warn("%s status to Down" % dest_addr)
            return False


def ReturnMsg(status,content):
    msg_subject = {
        'status': status,
        'content': content
    }
    return json.dumps(msg_subject)


class ThreadedTCPRequestHandler(SRH):
    #def GetaTtr(self,arg1,arg2):
    #    return getattr(self._object,arg1,'error')(**arg2)

    def handle(self):
        pass


class ThreadedTCPServer(TMI,TCP):
    pass


class Server(Daemon):
    def conf(self,host,port):
        self.host = host
        self.port = port
        ThreadedTCPServer.allow_reuse_address = True

    def run(self):
        #ThreadedTCPRequestHandler._object = self.obj
        #server = ThreadedTCPServer((self.host, self.port), ThreadedTCPRequestHandler)
        #blog.info('waiting for connection...')
        #server_thread = threading.Thread(target=server.serve_forever())
        #server_thread.setDaemon(True)
        #server_thread.start()
        #server.serve_forever()

        while True:
            pass
        pass

if __name__ == '__main__':
    HOST = config.getGalaxy("host")
    PORT = int(config.getGalaxy("port"))
    PID_FILE = config.getGalaxy("pid_file")
    mysql_socket = config.getMysql("socket")
    if mysql_socket:
        MYSQL = MySQL(config.getMysql("host"),config.getMysql("user"),config.getMysql("password"),
                      config.getMysql("galaxy"),mysql_socket)
    else:
        MYSQL = MySQL(config.getMysql("host"),config.getMysql("user"),config.getMysql("password"),
                      config.getMysql("galaxy"))

    server = Server(PID_FILE)
    server.conf(HOST,PORT)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            server.start()
        elif 'stop' == sys.argv[1]:
            server.stop()
        elif 'restart' == sys.argv[1]:
            server.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
