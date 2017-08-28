# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: ����selectģ��ʵ�ֶ�ͻ������ӣ���Ϊ�첽����ģʽ,
��������select������
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
    selectģ�ͣ�
    inputsΪ�ȴ���ȡ�Ķ�����У�
    outputsΪ�ȴ�д��Ķ�����У�
    ����������Ϊ�ȴ��쳣�Ķ�����У�
    ���ĸ�����Ϊ�ȴ�ָ��ʱ�䣬��λΪs����Ϊ��ѡ����
    ����ֵΪһ����Ԫ���飬���е�һ��Ԫ��Ϊ�ɶ�ȡ���󣬵ڶ���Ϊ��д����󣬵�����Ϊ�����쳣�Ķ���
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