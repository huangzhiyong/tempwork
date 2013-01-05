#!/usr/bin/env python
import threading
import sys
from galaxy_agent.lib.globaldef import  config
from galaxy_agent.lib.daemon import Daemon
from galaxy_agent.lib.galaxy_sock import ThreadTcpServer as TTS,MyRequestHandle

HOST = config.getGalaxy("host")
PORT = config.getGalaxy("port")
PID_FILE = config.getGalaxy("pid_file")
ADDR = (HOST,PORT)

class galaxy_daemon(Daemon):
    def run(self):
        server = TTS(ADDR,MyRequestHandle)
        print 'waiting for connection...'
        server_thread = threading.Thread(target = server.serve_forever())
        server_thread.setDaemon(True)
        server_thread.start()
        #print 'waiting for connection...'
        server.serve_forever()

if __name__ == "__main__":
    galaxy = Daemon(PID_FILE)
    if len(sys.argv) == 2:
        if sys.argv[1] == 'start':
            galaxy.start()
        elif sys.argv[1] == 'stop':
            galaxy.stop()
        elif sys.argv[1] == 'restart':
            galaxy.stop()
            galaxy.start()
        else:
            print "Unknown command..."
            sys.exit(2)
        sys.exit(0)
    else:
        print "Usage:%s start|stop|restart" % (sys.argv[0])