#-*- coding: utf-8 -*-
'''
Auther: Wood
Date: 2017-09-06
Desc: mysql连接器的实现
'''

import time, uuid, functools, threading, logging

# global engine object:
engine = None    

#扩展py中字典类型
class Dict(dict):
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

#定义异常        
class DBError(Exception):
    pass

class MultiColumnsError(DBError):
    pass

class _LazyConnection(object):

    '''
    管理数据库连接生命期，从engine获取连接
    cursor: 连接的游标
    commit: 提交修改
    rollback: 回滚
    cleanup: 清理连接
    '''

    def __init__(self):
        self.connection = None

    def cursor(self):
        if self.connection is None:
            connection = engine.connect()
            logging.info('open connection <%s>...' % hex(id(connection)))
            self.connection = connection
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def cleanup(self):
        if self.connection:
            connection = self.connection
            self.connection = None
            logging.info('close connection <%s>...' % hex(id(connection)))
            connection.close()
  
class _Engine(object):

    '''
    property:
        _connect: 数据连接的抽象
    method:
        connect: 执行数据库连接方法
    '''
    def __init__(self, connect):
        self._connect = connect

    def connect(self):
        return self._connect()  

'''
创建一个threadlocal 对象，对于不同的线程，使用不同的数据库链接
'''  
class _DbCtx(threading.local):
    '''
    连接信息保存在此对象中
    '''
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        logging.info('open lazy connection...')
        self.connection = _LazyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()

    def cursor(self):
        return self.connection.cursor()

#thread-local变量
_db_ctx = _DbCtx()
        
 class _ConnectionCtx(object):
    '''
    _ConnectionCtx object that can open and close connection context. _ConnectionCtx object can be nested and only the most 
    outer connection has effect.

    with connection():
        pass
        with connection():
            pass
    '''
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()

def connection():
    '''
    Return _ConnectionCtx object that can be used by 'with' statement:

    with connection():
        pass
    '''
    return _ConnectionCtx()

def with_connection(func):
    '''
    Decorator for reuse connection.

    @with_connection
    def foo(*args, **kw):
        f1()
        f2()
        f3()
    '''
    @functools.wraps(func)
    def _wrapper(*args, **kw):
        with _ConnectionCtx():
            return func(*args, **kw)
    return _wrapper
    
if __name__ == '__main__':
    d = Dict(('a', 'b'), (1,2), a=5, c=6)
    print d.a