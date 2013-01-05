#!/usr/bin/env python
import os,sys
import Queue
import logging
import logging.config
import ConfigParser

#current work path
CUR_PATH = sys.path[0] + os.sep

#config files location
LOG_CFG = CUR_PATH + "../conf/logger.cfg"
GALAXY_CFG = CUR_PATH + "../conf/galaxy_agent.cfg"
LOG_FILE = CUR_PATH + "../log/galaxy_agent.log"


#get the global logger
logging.config.fileConfig(LOG_CFG)
blog = logging.getLogger('backup')

# define config file parser class
class Config(object):
    def __init__(self):
        self.__parser = ConfigParser.ConfigParser()
        self.__configFile = GALAXY_CFG
        self.__rsync = "rsync"
        self.__mysql = "mysql"
        self.__galaxy = "galaxy"
        self.__xtrabackup = "xtrabackup"
        self.__remote = "remote"
        self.__nc = "nc"
        self.__backup = "backup"

    def __getValue(self,sec,key):
        if not sec or not key:
            blog.error("Invalid parameter. [sec]: %s, [key]: %s" % (sec,key))
            return False

        try:
            fp = open(self.__configFile)
            self.__parser.readfp(fp)
            value = self.__parser.get(sec,key)
            if not value:
                value = None
            fp.close()
        except Exception,e:
            blog.critical("Exception caught, [Exception]: %s" % e)
            return False
        else:
            return value

    def getGalaxy(self,key):
        return self.__getValue(self.__galaxy,key)

    def getRsync(self,key):
        return self.__getValue(self.__rsync,key)

    def getXtrabackup(self,key):
        return self.__getValue(self.__xtrabackup,key)

    def getRemote(self,key):
        return self.__getValue(self.__remote,key)

    def getMysql(self,key):
        return self.__getValue(self.__mysql,key)

    def getBackup(self,key):
        return self.__getValue(self.__backup,key)

    def getDynamic(self,sec,key):
        return self.__getValue(sec,key)

        # define Global Config object

config = Config()

# define the backup work Queue
BAK_QUEUE = Queue.Queue()