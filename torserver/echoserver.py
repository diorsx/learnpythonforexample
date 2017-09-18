# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-09-18
Desc: 测试tornado的TcpServer
'''

from tornado.tcpserver import TCPServer
from tornado.ioloop import IOLoop
from tornado.iostream import StreamClosedError
from tornado.options import define, options
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
import tornado.options
import time
import datetime
import logging

#定义常量
define("port", default=8091, type=int)

#初始化日志组件
def init_logging():  
    logger = logging.getLogger()  
    logger.setLevel(logging.DEBUG)  
  
    sh = logging.StreamHandler()  
  
    formatter = logging.Formatter('%(asctime)s -%(module)s:%(filename)s-L%(lineno)d-%(levelname)s: %(message)s')  
    sh.setFormatter(formatter)  
  
    logger.addHandler(sh)  
    logging.info("Current log level is : %s", logging.getLevelName(logger.getEffectiveLevel()))  
  

class echoServer(TCPServer):
    #gen.coroutine tornada框架中的装饰器, 被装饰的函数通过yield返回一个Future对象
    #gen.coroutine 化异步为同步过程
    @gen.coroutine
    def handle_stream(self, cli_sock, cli_addr):
        logging.info('The connection is from IP:{0}, port:{1}'.format(cli_addr[0], cli_addr[1]))
        while True:
            try:
                data = yield cli_sock.read_until(b"\n")
                logging.info("Received data at {0}：{1}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), data))
                yield cli_sock.write('Send data: {0}'.format(data))
            except StreamClosedError, msg:
                logging.info('Error msg: {0}'.format(msg))
                cli_sock.close()
                break

if __name__ == "__main__":
    init_logging()
    tornado.options.parse_command_line()
    try:
        server = echoServer()
        server.listen(options.port, address="0.0.0.0")
        logging.info('The Server is running at port {0}'.format(options.port))
    except:
        raise 
    IOLoop.instance().start()