#!/usr/bin/env python
import os
import logging
import logging.config
import ConfigParser

#current work path
CURR_PATH = os.path[0] + os.sep

#config files location
LOG_FILE = CURR_PATH + "../conf/logger.cfg"
CONF_FILE = CURR_PATH + "../conf/galaxy_agent.cfg"

#get the global logger
logging.config.fileConfig(LOG_FILE)
blog = logging.getLogger('backup')

# define config file parser class
class Config(object):
    def __init__(self):
        self.__parser = ConfigParser.ConfigParser()
        self.__configFile = CONF_FILE
        self.__info = "galaxy"

    def __getValue(self,sec,key):
        if not sec or not key:
            blog.error("Invalid parameter. [sec]: %s, [key]: %s" % (sec,key))
            return False

        try:
            fp = open(self.__configFile)
            self.__parser.readfp(fp)
            value = self.__parser.get(sec,key)
            fp.close()
        except Exception,e:
            blog.critical("Exception caught, [Exception]: %s" % e)
            return False
        else:
            return value

    def getGalaxy(self,key):
        return self.__getValue(self.__info,key)

# define Global Config object
config = Config()