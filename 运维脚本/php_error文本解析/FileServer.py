#!/bin/env python
# -*-coding:utf-8-*-
# Date: Tue Oct 18 2016 09:59:22 GMT+0800
# @Author: WoodLi
# @version: 0.0

__version__ = "0.0"
from BaseServer import BaseMonitorServer, BaseLineHandle
import redis
import hashlib
import json
import re
import time
import socket
import threading
import time
import os
import sys
import atexit
import string
from signal import SIGTERM


class FileMonitorServer(BaseMonitorServer):
    """docstring for FileMonitorServer"""

    def __init__(self, file_path, LineHandleClass, domainName, redisServer, errLevel):
        super(FileMonitorServer, self).__init__(file_path, LineHandleClass)
        self.host = socket.gethostname()
        self.domainName = domainName
        self.keys = self.domainName.keys()
        self.redisServer = redisServer
        self.errLevel = errLevel
        self.count = 0
        self.init_redis()

    def init_server(self):
        self.structDataRe = r'\[(.*)\] PHP (.*):  (.*) in (.*) on line (.*)'
        self.errContentRe = re.compile("\[.*\] ")

    def init_redis(self):
        pool = redis.ConnectionPool(host=self.redisServer['host'], port=self.redisServer['port'])
        self.rc = redis.StrictRedis(connection_pool=pool)

    def verify_line(self):
        self.lineResult = re.findall(self.structDataRe, self.line.strip('\n'), re.S)
        if self.lineResult:
            self.lineArray = self.lineResult[0]
            self.errContent = re.sub(self.errContentRe, '', self.line.strip('\n'))
            return True
        else:
            return False

    def make_errHash(self, errContent):
        myMd5 = hashlib.md5()
        myMd5.update(errContent)
        myMd5_str = myMd5.hexdigest()
        return myMd5_str

    def make_errDomain(self, errFile):
        errDomainName = ''
        for key in self.keys:
            if errFile.find(key) >= 0:
                errDomainName = self.domainName.get(key, 'unknown')
                break
        return True and errDomainName or 'unknown'


class FileLineHandle(BaseLineHandle):
    """docstring for FileLineHandle"""

    def __init__(self, lineArray, errContent, server):
        super(FileLineHandle, self).__init__(lineArray, errContent, server)

    def setup(self):
        self.errTime = int(time.time()) * 1000
        self.errLevel = self.lineArray[1]
        self.errReason = self.lineArray[2]
        self.errFile = self.lineArray[3]
        self.errLine = self.lineArray[4]
        self.errHash = self.server.make_errHash(self.errContent)

    def handle(self):
        self.errType = True and self.server.errLevel.get(self.errLevel, 4)
        if self.errType < 2047:
            self.errDomainName = self.server.make_errDomain(self.errFile)
            self.errObjMing = {
                "msgCode": 10001,
                "msg": {
                    "host": self.server.host,
                    "proj": self.errDomainName,
                    "file": self.errFile,
                    "line": self.errLine,
                    "time": self.errTime,
                    "type": self.errType,
                    "text": self.server.errContent,
                    "hash": self.errHash
                }
            }
            # self.errObjQu = {
            #     "errtime":self.errTime,
            #     "errlevel":self.errType,
            #     "errhost":self.server.host,
            #     "errdomain":self.errDomainName,
            #     "errreason":"Test",
            #     "errfile":self.errFile,
            #     "errhash":self.errHash,
            #     "errcontent":self.server.errContent
            # }

    def finish(self):
        if self.errObjMing or self.errObjQu:
            self.server.rc.publish('php_test', json.dumps(self.errObjMing))
            # self.server.rc.publish('php_error',json.dumps(self.errObjQu))


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
        so = file(self.stdout, 'w+')
        se = file(self.stderr, 'w+', 0)
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
    domainName = {
        "WEBTest": {
            "/var/www/html/webtest/": "test.test.com",
        }
    }
    redisServer = {'host': '192.168.2.201', 'port': 6379}
    errLevel = {
        "Fatal error": 8,
        "Warning": 4,
        "Parse error": 4,
        "Notice": 4
    }
    app = FileMonitorServer(r'/home/log/php_errors.log', FileLineHandle, domainName['WEBTest'], redisServer, errLevel)
    app.server_forever()

#解析命令行参数
def _args_parser():
    import argparse
    parser = argparse.ArgumentParser()
    #添加位置参数，参数值可为stop, start, restart
    parser.add_argument('action', choices=['stop', 'start', 'restart'])
    parser.add_argument('--daemon', '-d', action='store_true', help='process running in the backend')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    stdin = '/dev/null'
    stdout = os.path.dirname(os.path.realpath(__file__)) + '/send_client.log'
    stderr = os.path.dirname(os.path.realpath(__file__)) + '/send_client.log'
    pidfile = r'/tmp/send_client_process.pid'

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