# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc:ÀûÓÃsocket´«Êä×Ö·û
'''


from socket import *
from time import ctime

HOST = ''
PORT = 21568
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print 'waiting for connection...'
    tcpCliSock, addr = tcpSerSock.accept()  
    print '...connected from:', addr

    while True:
        try:
            data = tcpCliSock.recv(BUFSIZ)  
            print '> {0}\n'.format(data)
            tcpCliSock.send('>[{0}] {1}\n'.format(ctime(), data))
        except:
            print 'disconnect from:', addr
            tcpCliSock.close()  
            break