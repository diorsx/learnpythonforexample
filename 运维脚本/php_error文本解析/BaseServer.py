#!/bin/env python
# -*-coding:utf-8-*-
# Date: Tue Oct 18 2016 09:59:22 GMT+0800
# @Author: Wood
# @version: 0.1, 增加多行的判断
#

__version__ = "0.1"
import threading
import time


class BaseMonitorServer(object):
    """docstring for MonitorServer"""

    def __init__(self, file_path, LineHandleClass):
        super(BaseMonitorServer, self).__init__()
        self.file_path = file_path
        self.LineHandleClass = LineHandleClass
        self.__is_shut_down = threading.Event()
        self.__shutdown_server = False
        self.lineArray = ''
        self.errContent = ''
        try:
            self.fd = open(self.file_path, 'r')
            self.fd.seek(0, 2)
        except IOError as err:
            print str(err)
        self.init_server()

    #    def server_forever(self, poll_interval=0.5):
    #        self.__is_shut_down.clear()
    #        try:
    #            while not self.__shutdown_server:
    #                lines = self.fd.readlines()
    #                if lines:
    #                    for line in lines:
    #                        self.line = line
    #                        self.lineArray = ''
    #                        self.errContent = ''
    #                        self._handle_line_noblock()
    #                time.sleep(0.5)
    #        finally:
    #            self.__shutdown_server = False
    #            self.__is_shut_down.set()

    def server_forever(self, poll_interval=0.1):
        self.__is_shut_down.clear()
        try:
            while not self.__shutdown_server:
                lines = self.fd.readlines()
                if lines:
                    linestr = ''.join(lines)
                    for line in linestr.split('\n['):
                        if not line.startswith('['):
                            self.line = '[' + line
                        else:
                            self.line = line
                        self._handle_line_noblock()
                time.sleep(poll_interval)
        finally:
            self.__shutdown_server = False
            self.__is_shut_down.set()

    def init_server(self):
        pass

    def shutdown(self):
        self.__shutdown_server = True
        self.__is_shut_down.wait()

    def _handle_line_noblock(self):
        if self.verify_line():
            try:
                self.process_line()
            except:
                pass
            finally:
                self.finish_line()

    def verify_line(self):
        return True

    def process_line(self):
        self.LineHandleClass(self.lineArray, self.errContent, self)

    def finish_line(self):
        pass


class BaseLineHandle(object):
    """docstring for FileHandleClass"""

    def __init__(self, lineArray, errContent, server):
        super(BaseLineHandle, self).__init__()
        self.lineArray = lineArray
        self.errContent = errContent
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def handle(self):
        pass

    def setup(self):
        pass

    def finish(self):
        pass