#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2018年7月16日12:00:00
Desc: 使用多线程测试Mongo查询性能
'''

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import time
import pymongo
import threading
import sys
import  Queue

MONGO_HOST = "xx.xx.xx.xxx"
MONGO_PORT = 10001
MONGO_USER = "usertest"
MONGO_PASS = "passwd"
THREAD_NUMBERS = 10

#继承线程类，实现线程功能
class TestConnectMongo(threading.Thread):

    def __init__(self, queue):
        self.queue = queue
        self._thread_stop = False
        super(TestConnectMongo, self).__init__()

    def run(self):
        while not self._thread_stop:
            try:
                mongo = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
                db = mongo.collectionstest
                db.authenticate(MONGO_USER, MONGO_PASS)
                db.config_mongodb_field.find_one({"config_name": "travel_config"}, max_time_ms=500)
            except Exception as e:
                print ("Exception, {0}".format(e))
            finally:
                mongo.close()
        self.queue.put(1)

    @property
    def stop_thread(self):
        return self._thread_stop

    @stop_thread.setter
    def stop_thread(self, value):
        if not isinstance(value, bool):
            raise ValueError('invalid value: %s' % value)
        self._thread_stop = value

#CTRl+C EXIT进程
def stop_main_thread():
    while True:
        try:
            time.sleep(1)
        except KeyBoardError as e:
            sys.exit(0)

if __name__ == '__main__':
    t = threading.Thread(target=stop_main_thread)
    t.setDaemon(True)
    t.start()

    #利用Queue实现线程池功能
    queue = Queue.Queue(THREAD_NUMBERS)
    for i in xrange(THREAD_NUMBERS):
        queue.put(i)
    while True:
        try:
            if queue.get(block=True, timeout=5) is not None:
                t = TestConnectMongo(queue)
                t.setDaemon(True)
                t.start()
        except Queue.Empty as e:
            pass