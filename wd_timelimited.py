# -*- coding: utf-8 -*-

'''
Author: wood
Date: 2017-07-15
Desc: 限制pyhon中函数的执行时间
把要执行的执行的函数放入线程中执行,若超过指定时间, 则杀死该线程
'''

import functools
from threading import Thread
import time

# 获取私有函数
ThreadStop = Thread._Thread__stop

# 定义异常类
class TimeoutException(Exception):
    pass
class RunableException(Exception):
    pass

# 构建一个装饰器，使用参数timeout指定函数运行时间
def timelimited(timeout):
    class TimeLimited(Thread):

        def __init__(self, func, *args, **kwargs):
            Thread.__init__(self)
            self._error = None
            self._func = func
            self._args = args
            self._kwargs = kwargs

        def run(self):
            try:
                self.result = self._func(*self._args, **self._kwargs)
            except Exception as e:
                self._error = RunableException("Runing function %s warning: %s" % (repr(self._func.__name__), str(e)))

        def stop(self):
            if self.isAlive():
                ThreadStop(self)

    def _outer(func):
        @functools.wraps(func)
        def _inner(*args, **kwargs):
            t = TimeLimited(func, *args, **kwargs)
            t.start()
            t.join(timeout)

            if t.isAlive():
                t.stop()
                raise TimeoutException('Timeout for function %s' % (repr(func.__name__)))
            if isinstance(t._error, RunableException):
                raise t._error
            if t._error is None:
                return t.result
        return _inner
    return _outer

@timelimited(10)
def fn_1(secs):
    time.sleep(secs)

# 主函数进行测试，结果符合预期
if __name__ == "__main__":
    print  "开始: %s" % time.strftime("%Y-%m-%d %H:%M:%S")
    try:
        result1 = fn_1(5)
        result2 = fn_1(15)
    except Exception as e:
        print str(e)

    print  "结束: %s" % time.strftime("%Y-%m-%d %H:%M:%S")