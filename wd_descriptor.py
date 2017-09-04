# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-09-04
Desc: 实现python描述器
'''

#定义了__get__, __set__, __del__方法类称为描述器
class Descriptor(object):  
    def __get__(self, obj, type=None):  
            return self.obj
    def __set__(self, obj, val):  
        self.obj = val
    def __delete__(self, obj):  
        print 'delete', self, obj  

d = Descriptor()
d.name = "Tom"
print "Descriptor {0}，It's name is {1}".format(Descriptor.__name__, d.name)

#使用描述器实现python的Property
class WdProperty(object):
    def __init__(self, fget=None, fset=None, fdel=None):
        super(WdProperty, self).__init__()
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
               
    def __get__(self, instance, cls):
        if self.fget is not None:
            return self.fget(instance)
        
    def __set__(self,instance, value):
        if self.fset is not None:
            self.fset(instance, value)
            
    def __delete__(self,instance):
        if self.fdel is not None:
            self.fdel(instance)
            
    def getter(self, fn):
        self.fget = fn
        
    def setter(self, fn):
        self.fset = fn
        
    def deler(self, fn):
        self.fdel = fn


class People:
    def __init__(self, name="Tom", age=5):
        self._name = name
        self._age = age
        
    @WdProperty
    def name(self):
        return self._name
    
    @name.setter
    def set_name(self, value):
        self._name = value
   
    def get_age(self):
        return self._age
      
    def set_age(self, value):
        self._age = age
    
    #使用描述器来修饰
    age = WdProperty(get_age, set_age)
       
people = People()
print "初始用户名: {0}, 初始年龄: {1}".format(people.name, people.age)

#通过描述器来修改属性
people.name = "Cat"
people.age = 16
print "修改后用户名: {0}, 修改后年龄: {1}".format(people.name, people.age)