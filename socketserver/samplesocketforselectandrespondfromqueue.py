#-*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-08-28
Desc: ����selectģ��ʵ�ֶ�ͻ������ӣ���Ϊ�첽����ģʽ,��������select������,��Ϣ�ظ�Ҳʹ��selectģ�͡�
'''

import socket  
import queue  
from select import select  

HOST = ''
PORT = 12580
SERVER_IP = (HOST, PORT)
  
# ����ͻ��˷��͹�������Ϣ,����Ϣ��������� 
data = {} 
message_queue = {}  
input_list = []  
output_list = []  
  
if __name__ == "__main__":  
    server = socket.socket()  
    server.bind(SERVER_IP)  
    server.listen(10)  
    # ����Ϊ������  
    server.setblocking(False)  
  
    # ��ʼ��������˼�������б�  
    input_list.append(server)  
  
    while True:  
        # ��ʼ select ����,��input_list�еķ����server���м���  
        stdinput, stdoutput, stderr = select(input_list, output_list, input_list)  
  
        # ѭ���ж��Ƿ��пͻ������ӽ���,���пͻ������ӽ���ʱselect������  
        for obj in stdinput:  
            # �жϵ�ǰ�������ǲ��Ƿ���˶���, �������Ķ����Ƿ���˶���ʱ,˵�����¿ͻ������ӽ�����  
            if obj == server:  
                # ���տͻ��˵�����, ��ȡ�ͻ��˶���Ϳͻ��˵�ַ��Ϣ  
                conn, addr = server.accept()  
                print("Client {0} connected! ".format(addr))  
                # ���ͻ��˶���Ҳ���뵽�������б���, ���ͻ��˷�����Ϣʱ select ������  
                input_list.append(conn)  
                # Ϊ���ӵĿͻ��˵�������һ����Ϣ���У���������ͻ��˷��͵���Ϣ  
                message_queue[conn] = queue.Queue()  
  
            else:  
                # ���ڿͻ������ӽ���ʱ����˽��տͻ����������󣬽��ͻ��˼��뵽�˼����б���(input_list)���ͻ��˷�����Ϣ������  
                # �����ж��Ƿ��ǿͻ��˶��󴥷�  
                try:  
                    recv_data = obj.recv(1024)  
                    # �ͻ���δ�Ͽ�
                    if recv_data:  
                        print("received {0} from client {1}".format(recv_data.decode(), addr))  
                        # ���յ�����Ϣ���뵽���ͻ��˵���Ϣ������  
                        message_queue[obj].put(recv_data)  
  
                        # ���ظ������ŵ�output�б��У���select����  
                        if obj not in output_list:  
                            output_list.append(obj)  
  
                except ConnectionResetError:  
                    # �ͻ��˶Ͽ������ˣ����ͻ��˵ļ�����input�б����Ƴ�  
                    input_list.remove(obj)  
                    # �Ƴ��ͻ��˶������Ϣ����  
                    del message_queue[obj]  
                    print("\n[input] Client  {0} disconnected".format(addr))  
  
        # �������û�пͻ�������,Ҳû�пͻ��˷�����Ϣʱ����ʼ�Է�����Ϣ�б���д����Ƿ���Ҫ������Ϣ  
        for sendobj in output_list:  
            try:  
                # �����Ϣ����������Ϣ,����Ϣ�����л�ȡҪ���͵���Ϣ  
                if not message_queue[sendobj].empty():  
                    # �Ӹÿͻ��˶������Ϣ�����л�ȡҪ���͵���Ϣ  
                    send_data = message_queue[sendobj].get()  
                    sendobj.sendall(send_data)  
                else:  
                    # �������Ƴ��ȴ���һ�οͻ��˷�����Ϣ  
                    output_list.remove(sendobj)
  
            except ConnectionResetError:  
                # �ͻ������ӶϿ���  
                del message_queue[sendobj]  
                output_list.remove(sendobj)  
                print("\n[output] Client  {0} disconnected".format(addr))  