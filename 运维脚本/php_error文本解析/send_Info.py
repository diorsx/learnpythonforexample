# -*-coding:utf-8-*-
# Date: Tue Oct 18 2016 09:59:22 GMT+0800
# @Author: WoodLi
# @version: 0.3

__version__ = "0.3"
__Auther__ = "wood"

'''
增加程序的daemon功能
增加命令行参数解析
'''

import threading
import redis
import json
import socket
import struct
import os
import sys
import time
import atexit
import string
from signal import SIGTERM

#定义常量
CHANNEL_NAME = ['php_test']

"""创建socket连接字
AF_INET{,6}: IP Internet Protocol sockets
SOCK_DGRAM: datagrams, e.g. UDP
"""
#创建UDP套接字，用于把msg发送到UDP服务器
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

class PbRedisServer(object):
    """订阅Redis频道
    结构化订阅的信息
    发送信息至UDP服务器
    """

    def __init__(self, redis_addr, send_addr, HandleClass):
        super(PbRedisServer, self).__init__()
        self.msgId = 0
        self.MTU = 1012
        self.redis_host = redis_addr['host'] if redis_addr.has_key('host') else '127.0.0.1'
        self.redis_port = redis_addr['port'] if redis_addr.has_key('port') else 6379
        self.send_addr = send_addr
        self.HandleClass = HandleClass
        self.__is_shut_down = threading.Event()
        self.__shutdown_server = False
        self.init_server()

    def init_server(self):
        self.rc = redis.Redis(host=self.redis_host, port=self.redis_port)
        self.ps = self.rc.pubsub()
        self.ps.subscribe(CHANNEL_NAME)
        try:
            self.f = open('./msgID.txt', 'a')
        except IOError as err:
            print 'The msgID.txt is not exist'

    def server_forever(self):
        self.__is_shut_down.clear()
        try:
            for item in self.ps.listen():
                self.item = item['data']
                if isinstance(self.item, str):
                    self._handle_line_noblock()
        finally:
            self.f.close()
            self.__shutdown_server = False
            self.__is_shut_down.set()

    def _handle_line_noblock(self):
        self.HandleClass(self.item, self)


class SendMsgHandleClass(object):
    """docstring for SendHandleClass"""

    def __init__(self, textJson, app):
        super(SendHandleClass, self).__init__()
        self.textStr = textJson
        self.app = app
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def setup(self):
        self.total_sendLen = len(self.textStr)
        self.bytes_array = []

    def handle(self):
        self.split_count = self.total_sendLen / self.app.MTU + 1
        for i in range(0, self.split_count):
            self.make_bytes(self.textStr[i * self.app.MTU:(i + 1) * self.app.MTU], i * self.app.MTU)

    def finish(self):
        for send_data in self.bytes_array:
            s.sendto(send_data, self.app.send_addr)
        self.app.msgId += 1
        # self.app.f.write(str(self.app.msgId)+' '+str(self.total_sendLen)+'\n')
        if self.total_sendLen > 600:
            sys.stdout.write('sendTotalCount: %d, sendAtTime: %s, sendContextLength: %d, sendContext: %s\n' % (
            self.app.msgId, time.ctime(), self.total_sendLen, self.textStr))
        else:
            sys.stdout.write('sendTotalCount: %d, sendAtTime: %s, sendContextLength: %d\n' % (
            self.app.msgId, time.ctime(), self.total_sendLen))
        sys.stdout.flush()

    def make_bytes(self, text, offset):
        self.bytes_array.append(struct.pack('!3L', self.app.msgId, self.total_sendLen, offset) + text)


'''将当前进程fork为一个守护进程

    注意：如果你的守护进程是由inetd启动的，不要这样做！inetd完成了
    所有需要做的事情，包括重定向标准文件描述符，需要做的事情只有
    chdir() 和 umask()了
'''


class Daemon(object):
    def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null', *args, **kwargs):
        # 需要获取调试信息，改为stdin='/dev/stdin', stdout='/dev/stdout', stderr='/dev/stderr'，以root身份运行。
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile
        super(Daemon, self).__init__(*args, **kwargs)

    def _daemonize(self):
        try:
            pid = os.fork()
            if pid > 0:
                # 退出主进程
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.chdir("/")
        os.setsid()
        os.umask(0)

        # 创建子进程
        try:
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed: %d (%s)\n' % (e.errno, e.strerror))
            sys.exit(1)

            # 重定向文件描述符
        sys.stdout.flush()
        sys.stderr.flush()
        si = file(self.stdin, 'r')
        so = file(self.stdout, 'a+')
        se = file(self.stderr, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

        # 创建processid文件
        atexit.register(self.delpid)
        pid = str(os.getpid())
        file(self.pidfile, 'w+').write('%s\n' % pid)

    def delpid(self):
        os.remove(self.pidfile)

    def start(self):
        # 检查pid文件是否存在以探测是否存在进程
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if pid:
            message = 'pidfile %s already exist. Daemon already running?\n'
            sys.stderr.write(message % self.pidfile)
            sys.exit(1)

        # 启动主进程
        self._daemonize()
        self._run()

    def stop(self):
        # 从pid文件中获取pid
        try:
            pf = file(self.pidfile, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = 'pidfile %s does not exist. Daemon not running?\n'
            sys.stderr.write(message % self.pidfile)
            return  # 重启不报错

        # 杀进程
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError, err:
            err = str(err)
            if err.find('No such process') > 0:
                if os.path.exists(self.pidfile):
                    os.remove(self.pidfile)
            else:
                sys.stdout.write('Daemon starting...')
                sys.stdout.write('%s' % err)
                sys.exit(1)

    def restart(self):
        self.stop()
        self.start()

    def _run(self):
        pass


class MyDaemon(Daemon):
    def _run(self):
        _main()


def _main():
    sys.stdout.write('The Daemon started with pid %d at %s\n' % (os.getpid(), time.ctime()))
    redis_addr = {'host': '127.0.0.1', 'port': 6379}
    send_addr = ('192.168.2.209', 2020)
    server = PbRedisServer(redis_addr, send_addr, SendMsgHandleClass)
    server.server_forever()

#解析命令行参数
def _args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    #添加位置参数，参数值可为stop, start, restart
    parser.add_argument('action')
    parser.add_argument('--daemon', '-d', action='store_true', help='把进程放入后台运行')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    stdin = '/dev/null'
    stdout = os.path.dirname(os.path.realpath(__file__)) + '/send_php_error.log'
    stderr = os.path.dirname(os.path.realpath(__file__)) + '/send_php_error.log'
    pidfile = r'/tmp/send_phperror_process.pid'

    args = _args_parser()
    if args.action == 'stop':
        daemonize = MyDaemon(pidfile, stdin=stdin, stdout=stdout, stderr=stderr)
        daemonize.stop()
    elif args.action == 'restart':
        daemonize = MyDaemon(pidfile, stdin=stdin, stdout=stdout, stderr=stderr)
        daemonize.restart()
    elif args.action == 'start' and args.daemon:
        daemonize = MyDaemon(pidfile, stdin=stdin, stdout=stdout, stderr=stderr)
        daemonize.start()
    elif args.action == 'start':
        _main()
    else:
        sys.stdout.write('Unknown command %s' % sys.argv[1])
        sys.exit(2)
        sys.exit(0)