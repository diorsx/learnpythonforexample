# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: 多线程版本的socket传输字符
'''
from socket import *
import threading
from time import ctime

HOST = ''
PORT = 12580
ADDR = (HOST, PORT)

def sockHandle(tcpCliSock, addr):
    tcpCliSock.settimeout(5000)
    while True:
        try:
            data = tcpCliSock.recv(1024)
            print 'client {0} say: {1}\n'.format(addr, data)
            tcpCliSock.send('msg: {0} {1}\n'.format(ctime(), data))
        except:
            print 'disconnect from:', addr
            tcpCliSock.close()  
            break            
            
def main():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(ADDR)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        thread = threading.Thread(target=sockHandle, args=(client, addr))
        thread.setDaemon(True)  
        thread.start()
     
if __name__ == '__main__':
    main()
        