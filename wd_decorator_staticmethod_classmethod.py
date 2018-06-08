#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2018年6月8日12:00:00
Desc: python装饰器在类方法，静态方法中的应用
'''

import  time

class Date(object):
    
    def __init__(self, year, month, day):
        self._year = year
        self._month = month
        self._day = day

    #使用类方法而不是使用静态方法，可以防止在类被继承的场景下，调用这些staticmethod类型的函数会创建基类或访问基类，造成类类型的硬编码
    @classmethod
    def now(cls):
        t=time.localtime()                            #获取结构化的时间格式
        return cls(t.tm_year, t.tm_mon, t.tm_mday)   #新建实例并且返回

    @classmethod
    def tomorrow(cls):
        t=time.localtime(time.time()+86400)
        return cls(t.tm_year,t.tm_mon,t.tm_mday)

    def __str__(self):
        return "Date {0}-{1}-{2}".format(self._year, self._month, self._day)

class DateFromStr(Date):

    def __init__(self, year, month, day):
        super(DateFromStr, self).__init__(year, month, day)

    @staticmethod
    def from_string(date_as_string):
        try:
            day, month, year = map(int, date_as_string.split('-'))
            return DateFromStr(day, month, year)
        except Exception as e:
            return None

date1 = DateFromStr.now()
print date1

data2 = DateFromStr.tomorrow()
print data2

data3 = DateFromStr.from_string('2018-6-06')
print data3