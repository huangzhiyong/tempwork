#!/usr/bin/env python

import time,threading
from galaxy.bin.ping import *
import signal

ping_timeout = 2
status_last = True
status_list = [1 for i in range(0,20)]
dest_ip = ''
tread_exit = False

def thread_exit(a,b):
    global tread_exit
    tread_exit = True


def ping_check(dest_addr):
    global status_list
    global dest_ip
    global tread_exit
    dest_ip = dest_addr
    while not tread_exit:
        print "ping %s with ..." % dest_addr,
        try:
            delay = do_one(dest_addr,ping_timeout,64)
        except Exception,err:
            print err
            print "Network error"
            time.sleep(1)
            continue
        if delay == None:
            status_list.insert(0,0)
            status_list.pop()
            print "failed. (timeout within %ssec.)" % ping_timeout
        else:
            delay = delay * 1000
            status_list.insert(0,1)
            status_list.pop()
            print "get ping in %0.4fms" % delay
            time.sleep(1)


def check_status():
    global status_list
    global status_last
    global dest_ip
    global tread_exit
    status_changed = False
    status_list_copy = status_list
    while not tread_exit:
        if status_list_copy[:5].count(1) == 5:
            status_now = True
        elif status_list_copy[:5].count(0) == 5 or status_list_copy.count(0) == 10:
            status_now = False
        if status_now != status_last:
            status_changed = True
        else:
            status_changed = False
        status_last = status_now
        if status_changed == True:
            if status_now == False:
                print dest_ip,"status to Down"
            elif status_now == True:
                print dest_ip,"status to Up"
                #print 'now status is: ', status_now
        time.sleep(0.3)

if __name__ == '__main__':
    signal.signal(signal.SIGINT,thread_exit)
    th_ping = threading.Thread(target = ping_check,args = ("172.20.150.3",))
    th_status = threading.Thread(target = check_status)
    th_ping.setDaemon(True)
    th_status.setDaemon(True)
    th_ping.start()
    th_status.start()
    while th_ping.isAlive() or th_status.isAlive():
        time.sleep(1)