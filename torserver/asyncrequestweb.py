# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-09-18
Desc: 测试tornado的异步请求
'''


from tornado.httpclient import AsyncHTTPClient
from tornado.concurrent import Future
from tornado import gen
from util import stop_loop, start_loop

#gen.coroutine tornada框架中的装饰器, 被装饰的函数通过yield返回一个Future对象
#gen.coroutine 化异步为同步过程
@gen.coroutine
def asyn_fetch_web(url):
    if not url.startswith("http://"):
        url = "http://" + url
    print "get data from {0}".format(url)
    http_client = AsyncHTTPClient()
    res = yield http_client.fetch(url)
    print "{0} result: {1}".format(url, res.code)


if __name__ == '__main__':

    for i in range(0, 10):   
        asyn_fetch_web('www.baidu.com')
    start_loop()
