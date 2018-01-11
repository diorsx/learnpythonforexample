#!/bin/python
#!-*- coding: utf-8 -*-

'''
Author: wood
Date: 2018-01-10
Desc: inspect模块的用法，适用于以下用途:
(1)对是否是模块，框架，函数等进行类型检查
(2)获取源码  
(3)获取类或函数的参数的信息  
(4)解析堆栈
'''

import sys
import inspect

def foo():
    pass

class Cat(object):
    def __init__ (self, name='kitty'):  
        self.name  = name  

    def sayHi(self):
        return '%s, says Hi!' %self.name

cat = Cat()

print inspect.ismodule(cat)
print inspect.isclass(cat)
print inspect.isfunction(cat.sayHi)
print inspect.ismethod(cat.sayHi)
print inspect.isbuiltin(cat)
print inspect.isroutine(cat.sayHi)
print inspect.getmro(Cat)

print "=============================="
print inspect.getsourcelines(Cat)
for name, obj in inspect.getmembers(cat, inspect.ismethod):
    print name, obj