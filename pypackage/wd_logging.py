#!/bin/python
#!-*- coding: utf-8 -*-

'''
Author: wood
Date: 2017-12-29
Desc: 学习python内建logging模块
日志级别关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG, NOTSET
'''
import os
import sys
import logging

#默认情况下将日志打印到屏幕，日志级别为WARNING
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')

DEBUG = 1
INFO = 2
WARNING = 4
ERROR = 8
CRITICAL = 16

def output(logger=None, msg=None, level=0):
    print msg
    if logger == None:
        logger = logging
    if level <= DEBUG:
        logger.debug(msg if msg else 'This is debug message')
    elif level <= INFO:
        logger.info(msg if msg else 'This is info message')
    elif level <= WARNING:
        logger.warning(msg if msg else 'This is warning message')
    elif level <= ERROR:
        logger.error(msg if msg else 'This is error message')
    elif level <= CRITICAL:
        logger.critical(msg if msg else 'This is critical message')
    else:
        logger.info(msg if msg else 'This is no level message')

#logging.basicConfig函数对日志的输出格式及方式做相关配置
#参数含义:
# filename: 指定日志文件名
# filemode: 和file函数意义相同，指定日志文件的打开模式，'w'或'a'
# format: 指定输出的格式和内容，format可以输出很多有用信息
#  %(levelno)s: 打印日志级别的数值
#  %(levelname)s: 打印日志级别名称
#  %(pathname)s: 打印当前执行程序的路径，其实就是sys.argv[0]
#  %(filename)s: 打印当前执行程序名
#  %(funcName)s: 打印日志的当前函数
#  %(lineno)d: 打印日志的当前行号
#  %(asctime)s: 打印日志的时间
#  %(thread)d: 打印线程ID
#  %(threadName)s: 打印线程名称
#  %(process)d: 打印进程ID
#  %(message)s: 打印日志信息
# datefmt: 指定时间格式，同time.strftime()
# level: 设置日志级别，默认为logging.WARNING
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S',
    filename=r'./myapp.log',
    filemode='w')

output(msg='=========logging默认模式============', level=INFO)
output(level=DEBUG)
output(level=INFO)
output(level=WARNING)
output(level=ERROR)
output(level=CRITICAL)

#定义一个StreamHandler，将DEBUG级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
ch = logging.StreamHandler(stream=None)
formatter = logging.Formatter('%(asctime)-5s: %(levelname)-8s %(message)s')
ch.setFormatter(formatter)
logger = logging.getLogger('test')
logger.setLevel(logging.DEBUG)
logger.addHandler(ch)

output(msg='=========StreamHandler============', level=INFO)
output(level=DEBUG)
output(level=INFO)
output(level=WARNING)
output(level=ERROR)
output(level=CRITICAL)

#定义FileHandler, 将DEBUG级别或更高的日志信息输出至磁盘文件
fh = logging.FileHandler(
    r'./myfh.log',          #指定存储日志的文件路径
    mode = 'a',             #指定打开日志的mode, a为append
    encoding=None,          #指定文件字符集, 默认为UTF-8
    delay = False
    )
formatter = logging.Formatter('%(asctime)-5s: %(levelname)-8s %(message)s')
fh.setFormatter(formatter)
logger = logging.getLogger('fh')
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)

output(msg='=========FileHandler============', level=INFO)
output(logger=logger, level=DEBUG)
output(logger=logger, level=INFO)
output(logger=logger, level=WARNING)
output(logger=logger, level=ERROR)
output(logger=logger, level=CRITICAL)


#定义RotatingFileHandler, 最多备份5个日志文件, 每个日志文件最大100M
from logging.handlers import RotatingFileHandler
rfh = RotatingFileHandler(r'./myrfh.log', maxBytes=100*1024*1024, backupCount=5)
formatter = logging.Formatter('%(asctime)-5s: %(levelname)-8s %(message)s')
rfh.setFormatter(formatter)
logger = logging.getLogger('rfh')
logger.setLevel(logging.DEBUG)
logger.addHandler(rfh)

output(msg='=========RotatingFileHandler============', level=INFO)
output(logger=logger, level=DEBUG)
output(logger=logger, level=INFO)
output(logger=logger, level=WARNING)
output(logger=logger, level=ERROR)
output(logger=logger, level=CRITICAL)

cls_sh = logging.StreamHandler                    #日志输出到流，可以是sys.stderr、sys.stdout或者文件
cls_fh = logging.FileHandler                      #日志输出到文件

#日志回滚方式，实际使用时用RotatingFileHandler和TimedRotatingFileHandler, logging.handlers.BaseRotatingHandler
cls_rfh = logging.handlers.RotatingFileHandler
cls_trfh = logging.handlers.TimedRotatingFileHandler

cls_sh = logging.handlers.SocketHandler            # 远程输出日志到TCP/IP sockets
cls_dh = logging.handlers.DatagramHandler          # 远程输出日志到UDP sockets
cls_smtph = logging.handlers.SMTPHandler           # 远程输出日志到邮件地址
cls_slh = logging.handlers.SysLogHandler           # 日志输出到syslog
cls_nelh = logging.handlers.NTEventLogHandler      # 远程输出日志到Windows NT/2000/XP的事件日志
cls_mh = logging.handlers.MemoryHandler            # 日志输出到内存中的制定buffer
cls_hh = logging.handlers.HTTPHandler              # 通过"GET"或"POST"远程输出到HTTP服务