#!/usr/bin/env python
#!-*- coding: utf-8 -*-
'''
@desc: 使用命令模式，用于进程的起停管理，通过监听文件内容的变化，来管理进程的启停
@Author: wood
@date: 2017年8月18日15:20:00
'''

__author__ = "wood"
__version__ = "v0.1"

import re
import os
import datetime
import pyinotify
import logging
import shutil
import subprocess

#常量管理
PROCESS_PATH = r'/var/www/html/test/'
PROCESS_NAME = 'test.sh'
START_COMMAND = "cd {0} && ./{1} {2}".format(PROCESS_PATH, PROCESS_NAME, "start")
STOP_COMMAND = "cd {0} && ./{1} {2}".format(PROCESS_PATH, PROCESS_NAME, "stop")

class ProcessInvoker(object):
    '''调用者角色
    持有命令类对象，并执行具体命令类对象
    '''
    def __init__(self, StartCmd, Stopcmd):
        self.__start_command = StartCmd
        self.__stop_command = Stopcmd

    def start(self):
        self.__start_command.execute()

    def stop(self):
        self.__stop_command.execute()

class ProcessManager(object):
    '''接受者角色
    实施请求相关的操作
    '''
    def start_process(self):
        subprocess.Popen(START_COMMAND, shell=True)

    def stop_process(self):
        subprocess.Popen(STOP_COMMAND, shell=True)

class ProcessCommand(object):
    '''抽象命令类
    声明执行操作的接口
    子类调用接收者相应的操作
    '''
    def __init__(self):
        pass
    def execute(self):
        pass

class StartProcessCommand(ProcessCommand):
    '''
    抽象命令类的子类，创建具体命令对象并设定它的接收者
    通常会持有接收者，并调用接收者的功能来完成命令要执行的操作
    '''

    def __init__(self, pm):
        self.__pm = pm

    def execute(self):
        self.pm.start_process()

class StopProcessCommand(ProcessCommand):
    '''抽象命令类的子类，创建具体命令对象并设定它的接收者
    通常会持有接收者，并调用接收者的功能来完成命令要执行的操作
    '''

    def __init__(self, pm):
        self.__pm = pm

    def execute(self):
        self.pm.stop_process()


class ProcessStatChanger(object):
    '''客户类'''

    def __init__(self):
        self.__pm = ProcessManager()
        self.__switchStart = StartProcessCommand(self.__pm)
        self.__switchStop = StopProcessCommand(self.__pm)
        self.__invoker = ProcessInvoker(self.__switchStart, self.__switchStop)

    def switch_stat(self, cmd):
        cmd = cmd.strip().upper()
        try:
            if cmd == "START":
                self.__invoker.start()
            elif cmd == "STOP":
                self.__invoker.stop()
            else:
                print 'Argument "START" or "STOP" is required'
        except Exception as msg:
            print "Exception occured:%s" % msg

#监控文件内容的变化，来启停进程
class MyEventHandler(pyinotify.ProcessEvent):
    '''
    自定义inotify的事件类
    '''

    def __init__(self, ProcessStatChanger):
        self.__stat_change =ProcessStatChanger()
        super(MyEventHandler, self).__init__(self)

    def process_IN_CREATE(self, event):
        pname = event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        pname = event.pathname
        fname = event.name
        if fname != "monitor.txt":
            return
        f = open(pname, 'r')
        content = f.read()
        self.__stat_change.switch_stat(content)

if __name__ == '__main__':
    wm = pyinotify.WatchManager()
    wm.add_watch(PROCESS_PATH, pyinotify.ALL_EVENTS, auto_add=False, rec=False)
    eh = MyEventHandler(ProcessStatChanger)

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()