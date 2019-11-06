#!/usr/bin/python
# -*- coding: UTF-8 -*-


from difoss_pybase.common_utils import *
from difoss_pybase.mysql_wrapper import MysqlWrapper

class SperatedDatabase(object):

    def __init__(self, cfg, logger=None):
        self.__cfg = cfg
        self.__logger = logger
        self.__db_connects = []         # Array of DB conncet
        self.__dbname_2_connect = {}    # database name -> db connect

        sperated_db_cfg = deep_into_dict( cfg, ['sperated-db'] )
        if sperated_db_cfg:
            for db_cfg, arr_dbname in sperated_db_cfg.items():
                if not db_cfg in cfg:
                    raise Exception('"%s" field MUST include in json config file, or this something wrong in "sperated-db" field setting.' % db_cfg)
                tmpDb = MysqlWrapper(logger)
                tmpDb.connect(**cfg[db_cfg])
                tmpDb.set_autocommit(True)
                # reocrd DB object in global variables
                self.__db_connects.append( tmpDb )
                for dbname in arr_dbname:
                    self.__dbname_2_connect[dbname] = tmpDb
        else:
            log('info', 'Use default config "db" field to all database access.')
            if not 'db' in cfg:
                raise Exception('"db" field MUST include in json config file when missing "sperated-db" field setting.')
            tmpDb = MysqlWrapper(logger)
            tmpDb.connect(**cfg['db'])
            tmpDb.set_autocommit(True)
            # reocrd DB object in global variables for every database
            self.__db_connects.append( tmpDb )
            self.__dbname_2_connect['*'] = tmpDb

    def __del__(self):
        self.__destroy()

    def __exit__(self):
        self.__destroy()

    def __destroy(self):
        for db in self.__db_connects:
            if db.is_connected():
                db.disconnect()
        self.__dbname_2_connect.clear() # clear __dbname_2_connect to prevent get() 

    def __str__(self):
        s  = '__db_connects: %s\n' % str(self.__db_connects)
        s += '__dbname_2_connect: %s' % str(self.__dbname_2_connect)
        return s

    def get(self, database='*'):
        if database in self.__dbname_2_connect:
            return self.__dbname_2_connect[database]
        if '*' in self.__dbname_2_connect:
            return self.__dbname_2_connect['*']
        raise Exception("Database named '%s' has not config yet." % database)

    def get_all(self):
        return self.__db_connects
