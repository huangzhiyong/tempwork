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
GALAXY_CFG = CUR_PATH + "../conf/galaxy.cfg"
LOG_FILE = CUR_PATH + "../log/galaxy.log"


#get the global logger
logging.config.fileConfig(LOG_CFG)
blog = logging.getLogger('backup')

# define config file parser class
class Config(object):
    def __init__(self):
        self.__parser = ConfigParser.ConfigParser()
        self.__configFile = GALAXY_CFG
        self.__mysql = "mysql"
        self.__galaxy = "galaxy"


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

    def getMysql(self,key):
        return self.__getValue(self.__mysql,key)

    def getGalaxy(self,key):
        return self.__getValue(self.__galaxy,key)

# define Global Config object
config = Config()

# define the backup work Queue
BAK_QUEUE = Queue.Queue()