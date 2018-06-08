#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: python装饰器在属性赋值中的应用
'''


class NormalStudent(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

student1 = NormalStudent('Lili', 60)

#普通学生类NormalStudent的实例，在对其属性赋值时，无法检查属性是否合法
student1.score = 59
student1.score = 101

#调用类函数对属性进行赋值，但写法不方便
class NoNormalStudent(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score
    def get_score(self):
        return self.__score
    def set_score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score

student2 = NoNormalStudent('Lili', 60)
student2.get_score()
student2.set_score(-1)
student2.set_score(101)

#Python支持高阶函数, 可以用装饰器函数把 get/set 方法“装饰”成属性调用
class NoNormalStudent(object):
    def __init__(self, name, score):
        self.name = name
        self.__score = score

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, score):
        if score < 0 or score > 100:
            raise ValueError('invalid score')
        self.__score = score

student3 = NoNormalStudent('Lili', 60)
#贿赂老师，修改分数
student3.score = 100
student3.score = 101
