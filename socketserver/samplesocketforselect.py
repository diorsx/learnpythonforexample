# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: 利用select模型实现多客户端连接，此为异步阻塞模式,
会阻塞在select函数上
'''

from socket import *
from time import ctime
import select

HOST = ''
PORT = 12580
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)
inputs=[tcpSerSock]
outputs=[]
data={}

print 'waiting for connection...'
while True:
    '''
    select模型，
    inputs为等待读取的对象队列，
    outputs为等待写入的对象队列，
    第三个参数为等待异常的对象队列，
    第四个参数为等待指定时间，单位为s，此为可选参数
    返回值为一个三元数组，其中第一个元素为可读取对象，第二个为可写入对象，第三个为发生异常的对象
    '''
    rlist, wlist, xlist=select.select(inputs,outputs,[],10)
    for r in rlist:
        if r is tcpSerSock: 
            tcpCliSock, addr = tcpSerSock.accept()  
            print '...connected from: {0}'.format(addr)
            inputs.append(tcpCliSock)
            outputs.append(tcpCliSock)
            data[tcpCliSock]=''
        else:
            reqdata=r.recv(1024)
            if reqdata =='\r\n' or reqdata =='\n':
                if data[r].find('quit') >=0:
                    inputs.remove(r)
                    outputs.remove(r)
                    data.pop(r)
                    r.close()
                else:
                    print 'client {0} say: {1}'.format(r, data[r])
                    r.send('{0} {1}\r\n'.format(ctime(), data[r]))
                    data[r]=''
            else:
                data[r]=data[r]+reqdata