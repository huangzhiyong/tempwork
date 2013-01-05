#!/usr/bin/env python
from SocketServer import TCPServer as TCP,StreamRequestHandler as SRH,ThreadingMixIn as TMI
import threading
from time import ctime

# define the response message
RESPONSE_OK = "ok"
RESPONSE_ERR = "error"

class MyRequestHandle(SRH):
    def handle(self):
        print '..conected from:',self.client_address
        parameter = self.rfile.readline().split(',')
        print parameter
        if int(parameter[0]) == 1 and len(parameter) == 3:
            t = threading.Thread(target = Print,args = (parameter[1],))
            t.start()
            self.wfile.write('[%s] OK' % (ctime()))


class ThreadTcpServer(TMI,TCP):
    pass


def Print(aa):
    file('/tmp/galaxy.txt','w').write(aa)