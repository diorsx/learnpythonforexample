#!/bin/python
#!-*- coding: utf-8 -*-

'''
Author: wood
Date: 2018-01-12
Desc: cmd模块是python中包含的一个公共模块, 用于交互式shell和其它命令解释器的基类
可以基于cmd模块自定义子类, 实现命令行接口（CLI）的交互式应用程序
'''

"""
cmd只要方法与属性如下:
方法:
(1) cmdloop()：类似与Tkinter的mainloop，运行Cmd解析器
(2) onecmd(str)：读取输入，并进行处理，通常不需要重载该函数，而是使用更加具体的do_command来执行特定的命令；
(3) emptyline()：当输入空行时调用该方法；
(4) default(line)：当无法识别输入的command时调用该方法；
(5) completedefault(text,line,begidx,endidx):如果不存在针对的complete_*()方法,
那么会调用该函数，该函数主要是用于tab补充，且只能在linux下使用。
(6) precmd(line)：命令line解析之前被调用该方法；
(7) postcmd(stop，line)：命令line解析之后被调用该方法；
(8) preloop()：cmdloop()运行之前调用该方法；
(9) postloop()：cmdloop()退出之后调用该方法；
(10) help_command()：对command命令的说明，其中command为可变字符

属性:
(1) prompt：交互式提示字符，也就是刚才的(Cmd)可以换成我们自己想要的字符
(2) intro：在进入交互式shell前输出的字符串，可以认定为标志语之类的;
"""


import os
import sys
import cmd

#sample example1
class sampleCli(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'Lgh>: '

    def do_hello(self, line):
        print "hello %s" %line

    def do_exit(self, line):
        return -1

    def default(self, line):
        print line

try:
    samplecli = sampleCli()
    cmd.Cmd.cmdloop(samplecli)
except KeyboardInterrupt:
    sys.exit(1)

#sample example2
#见ansible-console的实现, 其run方法加载了cli.console下consoleCli类
#consoleCli类继承了cmd.Cmd类