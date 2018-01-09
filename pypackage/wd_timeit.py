#!/bin/python
#!-*- coding: utf-8 -*-

'''
Author: wood
Date: 2018-01-09
Desc: timeit为python中的计时器, 可以度量语句,函数执行的数据
'''

import timeit

#x=1语句的执行时间
print timeit.timeit('x=1')

#执行10000次的时间
print timeit.timeit('x=1', number=10000)

#列表生成器的执行时间,执行1次
print timeit.timeit('[i for i in range(10000)]', number=1)

#列表生成器的执行时间,执行10000次
print timeit.timeit('[i for i in range(100) if i%2==0]', number=10000)

#测试函数执行时间
def func():
    s = 0
    for i in range(1000):
        s += i

t1 = timeit.repeat('func()', 'from __main__ import func', number=100, repeat=5)
print t1

t2 = timeit.repeat(func, number=100, repeat=5)
print t2