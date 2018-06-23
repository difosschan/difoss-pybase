#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

# Use MySQL Connector/Python API
#import mysql.connector as msc
from mysql.connector import MySQLConnection
import sys, os, time
import json
import logging


class MysqlWrapper( MySQLConnection ):

    def __init__(self, logger=None):
        MySQLConnection.__init__(self)

        self.__logger = logger
        self.__last_descriptions = []
        self.__is_autocommit = False
        self.__type_2_function = {
            'insert': 'insert',
            'delete': 'delete',
            'update': 'update',
            'select': 'select',

            'desc': 'select',
            'show': 'select'
        }
        self.__types_max_len = 0
        for k in self.__type_2_function.iterkeys():
            self.__types_max_len = max(self.__types_max_len, len(k))

    @staticmethod
    def join(sql, arg=None):
        if not arg:
            return sql

        if isinstance(arg, dict):
            return '%s with arg: %s' % (sql, arg.__str__())  # TODO: arg is a dict is more complete

        sql_to_file = ''
        sql = sql.replace('%s', "'%s'")
        sql_list = sql.split('%s')
        for idx, p in enumerate(arg):
            sql_to_file += (sql_list[idx] + p.__str__())
        d = len(sql_list) - len(arg)
        if d > 0:
            sql_to_file += ''.join(sql_list[-1])
        return sql_to_file

    def set_autocommit(self, isAutoCommit):
        self.__is_autocommit = isAutoCommit
        
    def set_logger(self, logger):
        self.__logger = logger

    def __print_debug(self, debug_str):
        if self.__logger:
            self.__logger.debug(debug_str)
        else:
            print('[DEBUG] %s' % debug_str)

    def __set_last_descriptions(self, cursor):
        self.__last_descriptions = []
        for field_desc in cursor.description:
            self.__last_descriptions.append(field_desc[0])

    def get_last_descriptions(self):
        return self.__last_descriptions

    def __execute(self, sql, arg=None, silent=False):
        if not silent:
            self.__print_debug('execute %s by SQL <%s>' % (self.guess_query_type(sql), self.join(sql, arg)) )
        cursor = self.cursor()
        cursor.execute(sql, arg)
        last_row_id = cursor.getlastrowid()
        cursor.close()
        if self.__is_autocommit:
            self.commit()
        return last_row_id

    def select_one(self, sql, arg=None, want_descriptions=False, silent=False):
        if not silent:
            self.__print_debug('execute %s by SQL <%s>' % ('select(one)', self.join(sql, arg)) )

        cursor = self.cursor()
        cursor.execute(sql, arg)
        res = cursor.fetchone()
                
        # FIXME: [DONE]
        # File "/usr/lib64/python2.7/site-packages/mysql/connector/connection.py", line 1059, in handle_unread_result
        # raise errors.InternalError("Unread result found")
        
        # abandon_rows = cursor.fetchall()
        if self.unread_result:
            self.get_rows()

        if len(self.__last_descriptions):
            self.__last_descriptions = []
        if want_descriptions:
            self.__set_last_descriptions(cursor)

        cursor.close()
        self.commit()
        return res

    def select(self, sql, arg=None, want_descriptions=False, silent=False):
        if not silent:
            self.__print_debug('execute %s by SQL <%s>' % (self.guess_query_type(sql), self.join(sql, arg)) )

        cursor = self.cursor()
        cursor.execute(sql, arg)
        rows = cursor.fetchall()

        if len(self.__last_descriptions):
            self._last_descriptions = []
        if want_descriptions:
            self.__set_last_descriptions(cursor)

        cursor.close()
        self.commit()
        return rows

    def insert(self, sql, arg=None, silent=False):
        return self.__execute(sql, arg, silent)

    def update(self, sql, arg=None, silent=False):
        return self.__execute(sql, arg, silent)

    # NOTE: You should ignore the return value.
    def delete(self, sql, arg=None, silent=False):
        return self.__execute(sql, arg, silent)

    def guess_query_type(self, sql):
        first_word = sql.split()[0].lower() # 1st word in lower of sql
        if self.__type_2_function.has_key(first_word):
            return self.__type_2_function[first_word]
        return first_word

    def smart_query(self, sql, arg=None, silent=False, want_descriptions=False):
        query_type = self.guess_query_type(sql)
        if query_type in self.__type_2_function:
            instancemethod_str = 'self.%s' % self.__type_2_function[query_type]
            #print type( eval( 'self.update' ))
            # (sql=sql, arg=arg, silent=silent, want_descriptions=True)
            if 'select' == query_type:
                return getattr(self, self.__type_2_function[query_type]) (sql=sql, arg=arg, silent=silent, want_descriptions=want_descriptions)
            else:
                return getattr(self, self.__type_2_function[query_type]) (sql=sql, arg=arg, silent=silent)

