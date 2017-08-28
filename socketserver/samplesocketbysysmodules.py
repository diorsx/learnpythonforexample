# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: ʹ�÷�װ��SocketServerģ�����tcp server����example���ж��ʵ��
'''
from SocketServer import TCPServer,BaseRequestHandler,StreamRequestHandler,ThreadingTCPServer,ForkingTCPServer
import traceback  

class MyBaseRequestHandlerr(BaseRequestHandler):  
    """ 
    #��BaseRequestHandler�̳У�����дhandle���� 
    """  
    def handle(self):  
        #ѭ����������ȡ�����Կͻ��˵�����  
        while True:  
            #���ͻ��������Ͽ�����ʱ��self.recv(1024)���׳��쳣  
            try:  
                #һ�ζ�ȡ1024�ֽ�,��ȥ�����˵Ŀհ��ַ�(�����ո�,TAB,\r,\n)  
                data = self.request.recv(1024).strip()  
                  
                #self.client_address�ǿͻ��˵�����(host, port)��Ԫ��  
                print "receive from ({0}): {1}".format(self.client_address, data)
                  
                #ת���ɴ�д��д��(������)�ͻ���  
                self.request.sendall(data.upper()+'\r\n')  
            except:  
                traceback.print_exc()  
                break  


class MyStreamRequestHandlerr(StreamRequestHandler):  
    """ 
    #�̳�StreamRequestHandler������дhandle���� 
    #��StreamRequestHandler�̳���BaseRequestHandler�� 
    """  
    def handle(self):  
        while True:  
            #�ͻ��������Ͽ�����ʱ��self.rfile.readline()���׳��쳣  
            try:  
                #self.rfile������socket._fileobject,��дģʽ��"rb",������  
                #read,readline,readlines,write(data),writelines(list),close,flush  
                data = self.rfile.readline().strip()  
                print "receive from ({0}): {1}".format(self.client_address, data)  
                  
                #self.wfile������socket._fileobject,��дģʽ��"wb"  
                self.wfile.write(data.upper()+'\r\n')  
            except:  
                traceback.print_exc()  
                break  
               
if __name__ == "__main__":  
    #telnet 127.0.0.1 9999  
    host = ""       #��������������ip,��localhost��������,��""  
    port = 12580     #�˿�  
    addr = (host, port)  
    flag=raw_input("��ѡ������ģʽ:")
    if flag=='1':
        #socket server 1:TCPServer+BaseRequestHandler,���ͻ������ӣ����ַ�����
        #����TCPServer����
        server = TCPServer(addr, MyBaseRequestHandlerr)  
        #�����������  
        server.serve_forever()  

    elif flag=='2':
        #socket server 2:���ͻ������ӣ����ַ�����
        server = TCPServer(addr, MyStreamRequestHandlerr)  
        server.serve_forever()  

    elif flag=='3':
        #socket server 3���ö��߳�ʵ�ֶ�ͻ������ӣ����ַ�����
        server = ThreadingTCPServer(addr, MyStreamRequestHandlerr)  
        server.serve_forever()
    elif flag=='4':
        #socket server 4���ö����ʵ�ֶ�ͻ������ӣ����ַ�����
        server = ForkingTCPServer(addr, MyStreamRequestHandlerr)
        server.serve_forever()
    else:
        print "������1-4���:"