#!/usr/bin/env python
#!-*- coding: utf-8 -*-

'''
@desc: 类似python下supervisor，但没有管理界面，用于监控系统Daemon进程,当Daemon进程异常退出时，再次启动进程，
此脚本没有常驻于系统中，须设置定时任务，可一分钟执行一次，后期考虑放在系统中常驻
@Author: wood
@date: Mon Dec  4 11:50:00 CST 2017
'''

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import fcntl
import textwrap
from struct import unpack, pack
from termios import TIOCGWINSZ

import re
import sys
import os
import yaml
import subprocess
from optparse import OptionParser

OUTPUT_COLOR = True

codeCodes = {
    'black': u'0;30', 'bright gray': u'0;37',
    'blue': u'0;34', 'white': u'1;37',
    'green': u'0;32', 'bright blue': u'1;34',
    'cyan': u'0;36', 'bright green': u'1;32',
    'red': u'0;31', 'bright cyan': u'1;36',
    'purple': u'0;35', 'bright red': u'1;31',
    'yellow': u'0;33', 'bright purple': u'1;35',
    'dark gray': u'1;30', 'bright yellow': u'1;33',
    'magenta': u'0;35', 'bright magenta': u'1;35',
    'normal': u'0',
}

COLOR_HIGHLIGHT = 'white'
COLOR_VERBOSE = 'blue'
COLOR_WARN = 'bright purple'
COLOR_ERROR = 'red'
COLOR_DEBUG = 'dark gray'
COLOR_DEPRECATE = 'purple'
COLOR_SKIP = 'cyan'
COLOR_UNREACHABLE = 'bright red'
COLOR_OK = 'green'
COLOR_CHANGED = 'yellow'
COLOR_DIFF_ADD = 'green'
COLOR_DIFF_REMOVE = 'red'
COLOR_DIFF_LINES = 'cyan'


def parsecolor(color):
    """SGR parameter string for the specified color name."""
    matches = re.match(r"color(?P<color>[0-9]+)"
                       r"|(?P<rgb>rgb(?P<red>[0-5])(?P<green>[0-5])(?P<blue>[0-5]))"
                       r"|gray(?P<gray>[0-9]+)", color)
    if not matches:
        return codeCodes[color]
    if matches.group('color'):
        return u'38;5;%d' % int(matches.group('color'))
    if matches.group('rgb'):
        return u'38;5;%d' % (16 + 36 * int(matches.group('red')) +
                             6 * int(matches.group('green')) +
                             int(matches.group('blue')))
    if matches.group('gray'):
        return u'38;5;%d' % (232 + int(matches.group('gray')))


def stringc(text, color):
    if OUTPUT_COLOR:
        color_code = parsecolor(color)
        return u"\n".join([u"\033[%sm%s\033[0m" % (color_code, t) for t in text.split(u'\n')])
    else:
        return text


class Display:

    def __init__(self, verbosity=0):

        self.columns = None
        self.verbosity = verbosity

        # list of all deprecation messages to prevent duplicate display
        self._deprecations = {}
        self._warns = {}
        self._errors = {}
        self._set_column_width()

    def display(self, msg, color=None, stderr=False):
        """ Display a message to the user
        Note: msg *must* be a unicode string to prevent UnicodeError tracebacks.
        """
        nocolor = msg
        if color:
            msg = stringc(msg, color)

        if not msg.endswith(u'\n'):
            msg2 = msg + u'\n'
        else:
            msg2 = msg

        if not stderr:
            fileobj = sys.stdout
        else:
            fileobj = sys.stderr

        fileobj.write(msg2)

    def debug(self, msg):
        self.display("%6d %0.5f: %s" % (os.getpid(), time.time(), msg), color=COLOR_DEBUG)

    def verbose(self, msg, host=None, caplevel=2):
        if self.verbosity > caplevel:
            if host is None:
                self.display(msg, color=COLOR_VERBOSE)
            else:
                self.display("<%s> %s" % (host, msg), color=COLOR_VERBOSE)

    def info(self, msg, formatted=False):
        if not formatted:
            new_msg = "\n[INFO]: %s" % msg
            wrapped = textwrap.wrap(new_msg, self.columns)
            new_msg = "\n".join(wrapped) + "\n"
        else:
            new_msg = "\n[INFO]: \n%s" % msg

        if new_msg:
            self.display(new_msg, color=COLOR_OK)

    def warning(self, msg, formatted=False):
        if not formatted:
            new_msg = "\n[WARNING]: %s" % msg
            wrapped = textwrap.wrap(new_msg, self.columns)
            new_msg = "\n".join(wrapped) + "\n"
        else:
            new_msg = "\n[WARNING]: \n%s" % msg

        if new_msg:
            self.display(new_msg, color=COLOR_WARN, stderr=True)

    def error(self, msg, wrap_text=True):
        if wrap_text:
            new_msg = u"\n[ERROR]: %s" % msg
            wrapped = textwrap.wrap(new_msg, self.columns)
            new_msg = u"\n".join(wrapped) + u"\n"
        else:
            new_msg = u"ERROR! %s" % msg
        if new_msg:
            self.display(new_msg, COLOR_ERROR, stderr=True)

    def _set_column_width(self):
        if os.isatty(0):
            tty_size = unpack('HHHH', fcntl.ioctl(0, TIOCGWINSZ, pack('HHHH', 0, 0, 0, 0)))[1]
        else:
            tty_size = 0
        self.columns = max(79, tty_size - 1)


display = Display()


def parse(argv):
    """Parse the command line args
    """
    usage = "usage: %prog [options] -f conffile"
    parser = OptionParser(usage=usage)
    parser.add_option("-f", "--conf", dest="filename", help="the configure file of process info", metavar="FILE")
    parser.add_option("-v", "--version", action="store_true", dest="verbose",
                      help="print product version and exit")
    (options, args) = parser.parse_args(argv)
    return options, args


def load_config_file(options):
    '''Load Process Config File(first found is used)
    '''
    basedir = os.path.dirname(__file__)
    path0 = getattr(options, 'filename', None)
    path1 = basedir + "/daemon_process.yml"
    path2 = os.path.expanduser("~/daemon_process.yml")
    path3 = r'/etc/daemon_process.yml'

    for path in [path0, path1, path2]:
        if path is not None and os.path.exists(path):
            try:
                f = open(path)
            except Exception, e:
                display.error(u"加载%s出错,错误信息: %s" % (path, e.msg))
                sys.exit(1)

            try:
                process_yaml = yaml.load(f)
            except Exception, e:
                display.error(u"解析yaml文件%s出错,错误信息: %s" % (path, e.msg))
                sys.exit(1)
            return process_yaml
    return {}


class Process(object):
    """
    进程类, 封装了start 进程时的各种参数
    """

    def __init__(self, *args, **kwargs):
        super(Process, self).__init__()
        self.args = args
        self._pro_path = kwargs['pro_path'] if kwargs.has_key('pro_path') else r'/root'
        self._pro_exec = kwargs['pro_exec'] if kwargs.has_key('pro_exec') else r'/bin/bash'
        self._pro_name = kwargs['pro_name'] if kwargs.has_key('pro_name') else r''
        self._pro_cmd = kwargs['pro_cmd'] if kwargs.has_key('pro_cmd') else r''
        self._pro_log = kwargs['pro_log'] if kwargs.has_key('pro_log') else r'/dev/null'
        self._enable = kwargs['enable'] if kwargs.has_key('enable') else True

    def _running(self):
        cmd = "ps -ef | grep %s | grep -v grep | wc -l" % self._pro_name
        if not self._pro_name:
            return 0
        else:
            process_count = os.popen(cmd).read()
            try:
                process_count = int(process_count)
                return process_count
            except Exception, e:
                display.error(e.msg)
                return 0

    def run(self, count=1):
        cmd = self.get_cmd()
        child_process_list = []
        running_process_count = self._running()
        if running_process_count < count and self._enable:
            imbalance = count - running_process_count
            for p in range(0, imbalance):
                child_process = subprocess.Popen(cmd, shell=True, cwd=self._pro_path)
                child_process_list.append(child_process.pid)
        return child_process_list

    def get_cmd(self):
        if self._pro_cmd:
            return self._pro_cmd
        else:
            return '{0} {1} >{2} 2>&1'.format(self._pro_exec, self._pro_name, self._pro_log)
    # cmd = property(get_cmd)
    # print cmd

class ProcessIterator(object):
    """进程迭代器
    """
    def __init__(self, config):
        super(ProcessIterator, self).__init__()
        self._config = config
        self._process_info = config['process'] if config.has_key('process') else []

    def __iter__(self):
        return self

    def next(self):
        if not self._process_info:
            raise StopIteration
        process_info = self._process_info.pop()
        p = Process(**process_info)
        return p

if __name__ == '__main__':
    basefile = sys.argv[0]
    argv = sys.argv[1:]
    options, args = parse(argv)
    if options.verbose:
        display.info("%s version 1.0" % os.path.basename(basefile))
        sys.exit(0)

    conf = load_config_file(options)
    for p in ProcessIterator(conf):
        p.run()