__author__ = 'Administrator'
from socket import *

HOST = '172.20.150.3'
PORT = 6868
BUFSIZ = 1024
ADDR = (HOST,PORT)

while True:
    data = raw_input('> ')
    if not data:
        break
    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    tcpCliSock.send('%s,\n' % data)
    data = tcpCliSock.recv(BUFSIZ)
    print data
    #print data.split('(')[1].split(',')[0]
    #if  data.split('(')[1].split(',')[0] != '\'Hello:\'':
    #   break
    #print "aaa",data.strip()
    tcpCliSock.close()
