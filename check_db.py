#-*- coding: utf-8 -*-

import db
import threading

USER = 'testacount'
PASSWORD = 'testpasswd'
HOST = '192.168.14.251'
PORT = 3306
DATABASE = 'USER'

'''
测试ORM
'''
class radgroupreply(db.Model):
    __table__ = 'radgroupreply'

    id = db.IntegerField(primary_key=True)
    groupname = db.StringField()
    attribute = db.StringField()
    op = db.StringField()

db.create_engine(user=USER, password=PASSWORD, database=DATABASE, host=HOST, port=PORT)
r = radgroupreply.find_all()

'''
测试多线程中数据库中数据查询
'''
class dataQueryThread(threading.Thread):
    '''
    '''
    def __init__(self, *args):
        super(dataQueryThread, self).__init__()
        self.setDaemon(False) 
        
    def run(self):
        print "{0} start".format(self.getName())
        result = radgroupreply.find_all()
        print "query result: {0}\n".format(result)

threads = list()

#create threads
for i in range(100):
    threads.append(dataQueryThread())
   
for t in threads:
    t.start()

# for t in threads:
#     t.join()