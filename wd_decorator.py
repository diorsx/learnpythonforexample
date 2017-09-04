#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: 实现python的装饰器
'''

import functools
import time
import logging
from threading import Thread
import signal

#构建不带参数的装饰器1
def logging_process(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        print("start called: %s" % func.__name__)
        result = func(*args, **kwargs)
        print("end called: %s" % func.__name__)
        return result
    return decorator

#构建不带参数的装饰器2
def fn_timer(func):
    @functools.wraps(func)
    def decorator(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        print "Total time running %s: %s seconds" %(func.__name__, t1-t0)
        return result
    return decorator

#同时使用装饰器
@logging_process
@fn_timer
def get_response(url="http://www.baidu.com"):
    import requests
    try:
        r = requests.get(url)
        print u"请求返回码：%s" %r.status_code
    except Exception, e:
        print "error: %s" %e

        
#构建带参数的装饰器1
def use_logging(level='warn'):
    if level == 'warn':
        print_log = logging.warn
    elif level == 'error':
        print_log = logging.error
    else:
        print_log = logging.info
    def _outer(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            print_log("Start {0} at {1}".format(func.__name__, time.ctime()))
            result = func(*args, **kwargs)
            print_log("End {0} at {1}".format(func.__name__, time.ctime()))
        return _inner
    return _outer
    

#使用带参数的装饰器
@use_logging(level='warn')
def get_response(url="http://www.baidu.com"):
    import requests
    try:
        r = requests.get(url)
        print u"请求返回码：%s" %r.status_code
    except Exception, e:
        print "error: %s" %e

#decorator with no parameters defined by class
class fn_timer_cls(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.t_start = time.time()
        self.result = self.func(*args, **kwargs)
        self.t_end = time.time()
        print "Total time running %s: %s seconds" %(self.func.__name__, self.t_end-self.t_start)
        return self.result

@fn_timer_cls
def get_response(url="http://www.baidu.com"):
    import requests
    try:
        r = requests.get(url)
        print u"请求返回码：%s" %r.status_code
    except Exception, e:
        print "error: %s" %e


# 装饰器实例: 结果缓存
def resultcache(type='mem'):
    def _outer(func):
        if type == 'mem':
            cache = {}
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            key = str(args)+str(kwargs)
            if key not in cache:
                cache[key] = func(*args, **kwargs)
            return cache[key]
        return _inner
    return _outer

#使用带参数的装饰器
@resultcache(type='mem')
def add(x=1, y=2):
    return x+y

