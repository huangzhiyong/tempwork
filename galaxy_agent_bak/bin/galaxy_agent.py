#!/usr/bin/env python
# - * - coding: utf-8 -*-
import threading
import sys,json
import traceback
from SocketServer import TCPServer as TCP,StreamRequestHandler as SRH,ThreadingMixIn as TMI
from galaxy_agent_bak.bin.globaldef import config,blog
from galaxy_agent_bak.bin.daemon import Daemon
from galaxy_agent_bak.bin.galaxy_method import Method

def ReturnMsg(status,content):
    msg_subject = {
        'status': status,
        'content': content
    }
    return json.dumps(msg_subject)


class ThreadedTCPRequestHandler(SRH):
    def GetaTtr(self,arg1,arg2):
        return getattr(self._object,arg1,'error')(**arg2)

    def handle(self):
        try:
            blog.info("...conected from: %s" % (str(self.client_address)))
            params = json.loads(self.request.recv(1024))
            blog.info('Has from the client accepts data...')
            #data = self.rfile.readline()
            if params:
                t = threading.Thread(target = self.GetaTtr,args = (params['Func'],params['Args']))
                t.setDaemon(True)
                t.start()
                blog.info("Begin to use %s function backup..." % (params['Func']))
                self.request.send(ReturnMsg(1,"starting backup"))
                #self.wfile.write('[%s] OK'%(time.ctime()))
            else:
                blog.error("The client transfer over parameters can't for empty!")
                self.request.send(ReturnMsg(0,"Parameters can't for empty"))
        except:
            self.request.send(ReturnMsg(0,traceback.format_exc()))
            blog.error('error in ThreadedTCPRequestHandler :%s, res:%s' % (traceback.format_exc(),str(params)))


class ThreadedTCPServer(TMI,TCP):
    pass


class Server(Daemon):
    def conf(self,host,port,obj):
        self.host = host
        self.port = port
        self.obj = obj
        ThreadedTCPServer.allow_reuse_address = True

    def run(self):
        ThreadedTCPRequestHandler._object = self.obj
        server = ThreadedTCPServer((self.host,self.port),ThreadedTCPRequestHandler)
        blog.info('waiting for connection...')
        #server_thread = threading.Thread(target=server.serve_forever())
        #server_thread.setDaemon(True)
        #server_thread.start()
        server.serve_forever()

if __name__ == '__main__':
    HOST = config.getGalaxy("host")
    PORT = int(config.getGalaxy("port"))
    PID_FILE = config.getGalaxy("pid_file")

    server = Server(PID_FILE)
    server.conf(HOST,PORT,Method)
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
