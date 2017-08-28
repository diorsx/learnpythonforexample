#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: 利用select模型实现多客户端连接，此为客户端模块.
'''


import socket

HOST='127.0.0.1'
PORT=12580

sockaddr=(HOST,PORT)
ct=socket.socket()
ct.connect(sockaddr)

while True:
    inp=input("请输入要发送的内容: ")
    ct.sendall(bytes(inp))
    ret_bytes=ct.recv(1024)
    print str(ret_bytes)
    
ct.close()