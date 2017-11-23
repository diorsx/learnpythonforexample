# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: 使用封装的SocketServer模块来搭建tcp server，此example中有多个实例
'''
from SocketServer import TCPServer,BaseRequestHandler,StreamRequestHandler,ThreadingTCPServer,ForkingTCPServer
import traceback  

class MyBaseRequestHandlerr(BaseRequestHandler):  
    """ 
    #从BaseRequestHandler继承，并重写handle方法 
    """  
    def handle(self):  
        #循环监听（读取）来自客户端的数据  
        while True:  
            #当客户端主动断开连接时，self.recv(1024)会抛出异常  
            try:  
                #一次读取1024字节,并去除两端的空白字符(包括空格,TAB,\r,\n)  
                data = self.request.recv(1024).strip()  
                  
                #self.client_address是客户端的连接(host, port)的元组  
                print "receive from ({0}): {1}".format(self.client_address, data)
                  
                #转换成大写后写回(发生到)客户端  
                self.request.sendall(data.upper()+'\r\n')  
            except:  
                traceback.print_exc()  
                break  


class MyStreamRequestHandlerr(StreamRequestHandler):  
    """ 
    #继承StreamRequestHandler，并重写handle方法 
    #（StreamRequestHandler继承自BaseRequestHandler） 
    """  
    def handle(self):  
        while True:  
            #客户端主动断开连接时，self.rfile.readline()会抛出异常  
            try:  
                #self.rfile类型是socket._fileobject,读写模式是"rb",方法有  
                #read,readline,readlines,write(data),writelines(list),close,flush  
                data = self.rfile.readline().strip()  
                print "receive from ({0}): {1}".format(self.client_address, data)  
                  
                #self.wfile类型是socket._fileobject,读写模式是"wb"  
                self.wfile.write(data.upper()+'\r\n')  
            except:  
                traceback.print_exc()  
                break  
               
if __name__ == "__main__":  
    #telnet 127.0.0.1 9999  
    host = ""       #主机名，可以是ip,像localhost的主机名,或""  
    port = 12580     #端口  
    addr = (host, port)  
    flag=raw_input("请选择运行模式:")
    if flag=='1':
        #socket server 1:TCPServer+BaseRequestHandler,单客户端连接，单字符接收
        #构造TCPServer对象
        server = TCPServer(addr, MyBaseRequestHandlerr)  
        #启动服务监听  
        server.serve_forever()  

    elif flag=='2':
        #socket server 2:单客户端连接，多字符接收
        server = TCPServer(addr, MyStreamRequestHandlerr)  
        server.serve_forever()  

    elif flag=='3':
        #socket server 3：用多线程实现多客户端连接，多字符接收
        server = ThreadingTCPServer(addr, MyStreamRequestHandlerr)  
        server.serve_forever()
    elif flag=='4':
        #socket server 4：用多进程实现多客户端连接，多字符接收
        server = ForkingTCPServer(addr, MyStreamRequestHandlerr)
        server.serve_forever()
    else:
        print "请输入1-4序号:"