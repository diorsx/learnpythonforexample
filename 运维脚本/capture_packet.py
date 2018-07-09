# -*- coding:utf-8 -*-
'''
Author: wood
Date: 2017-11-19
Desc: 抓包分析，熟悉各协议包的头部格式
'''

import pcap
import dpkt
import struct
import socket
import ctypes
from ctypes import *

num2hex = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'
        }

class Ethernet(ctypes.Structure):
    '''
    Data link layer, to resolve MAC Frame header
    dest: 目的mac地址
    src: 源mac地址
    '''
    _protocols_ = {8: "IP", 1544: "ARP"}
    _fields_ = [
        ("dest",    ctypes.c_ubyte * 6),
        ("src",     ctypes.c_ubyte * 6),
        ("type",    ctypes.c_ushort),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        '''
        解析field字段
        '''
        self.dest_address = self.bytearray_to_character(self.dest)
        self.src_address = self.bytearray_to_character(self.src)
        try:
            self.protocol = self._protocols_[self.type]
        except:
            self.protocol = str(self.type)

    def __str__(self):
        return "Next layer protocol type: {0}, dest mac: {1}, src mac: {2}".format(self.protocol, self.dest_address, self.src_address)

    def bytearray_to_character(self, c_bytearray):
        '''
        convert bytearray to mac address
        Args:
            c_bytearray: six byte array for c language
        Returns:
            Human-readable mac address
            example:
                00:1A:2B:3C:4D:5F
        '''
        human_readable_address = ''
        for c_byte in c_bytearray:
            ch1 = num2hex.get((c_byte >> 4))
            ch2 = num2hex.get(c_byte & 0b00001111)
            human_readable_address = human_readable_address + ch1 + ch2 + ":"
        return human_readable_address


class IP(ctypes.Structure):
    '''
    Network layer, to resolve IP header
    versionandheaderlen: 版本信息(前4位)，头长度(后4位)
    tos: 服务类型8位
    totallen: 数据包长度
    packetid: 数据包标识
    sliceinfo: 分片使用
    ttl: 包存活时间
    type: 协议类型
    checksum: 校验和
    src: SourIp
    dest: DestIp
    '''
    _protocols_ = { 1: "ICMP", 6: "TCP", 17: "UDP" }
    _fields_ = [
        ("versionandheaderlen",  ctypes.c_ubyte),
        ("tos",                  ctypes.c_ubyte),
        ("totallen",             ctypes.c_ushort), 
        ("packetid",             ctypes.c_ushort), 
        ("sliceinfo",            ctypes.c_ushort),
        ("ttl",                  ctypes.c_ubyte),
        ("type",                 ctypes.c_ubyte), 
        ("checksum",             ctypes.c_ushort),
        ("src",                  ctypes.c_uint),
        ("dest",                 ctypes.c_uint),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        #解析源IP和目的IP
        self.src_address = socket.inet_ntoa(struct.pack("<I", self.src))
        self.dest_address = socket.inet_ntoa(struct.pack("<I", self.dest))

        #解析版本号与首部长度
        self.version = (self.versionandheaderlen >> 4) & 0b00001111
        self.ihl = (self.versionandheaderlen & 0b00001111 ) * 4

        #解析数据报总长度,包ID和TTL
        self.totallen = struct.unpack(">I", struct.pack("<I", self.totallen))[0]
        self.packetid = struct.unpack(">H", struct.pack("<H", self.packetid))[0]
        self.ttl = struct.unpack(">H", struct.pack("<H", self.ttl))[0]

        #解析四层协议
        try:
            self.protocol = self._protocols_[self.type]
        except:
            self.protocol = str(self.type)

    def __str__(self):
        return "Next layer protocol type: {0}, dest ip: {1}, src ip: {2}, packet ttl: {3}".format(
            self.protocol, self.dest_address, self.src_address, self.ttl)

class TCP(ctypes.Structure):
    '''
    Transport layer, to resolve TCP header
    src: 源端口号16bit
    dest: 目的端口号16bit
    sequnum: 序列号32bit
    acknowledgenum: 确认号32bit
    headerlenandflag: 前4位：TCP头长度；中6位：保留；后6位：标志位
    windowsize: 窗口大小16bit
    checksum: 检验和16bit
    urgentpointer: 紧急数据偏移量16bit
    '''
    _fields_ = [
        ("src",              ctypes.c_ushort),
        ("dest",             ctypes.c_ushort),
        ("sequnum",          ctypes.c_uint),
        ("acknowledgenum",   ctypes.c_uint),
        ("headerlenandflag", ctypes.c_ushort), 
        ("windowsize",       ctypes.c_ushort),
        ("checksum",         ctypes.c_ushort),
        ("urgentpointer",    ctypes.c_ushort),
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        #解析端口, 80端口字节流为0x00 0x50, 
        #当系统接收到此字节流时，会按小端模式解析成ushort类型
        #由于网络字节序为大端模式，需把ushort解析成大端模式
        self.src_port = struct.unpack(">H", struct.pack("<H",self.src))[0]
        self.dest_port = struct.unpack(">H", struct.pack("<H",self.dest))[0]

        #解析TCP首部长度与标志位
        self.headerlenandflag = struct.unpack(">H", struct.pack("<H", self.headerlenandflag))[0]
        self.thl = (self.headerlenandflag >> 12) *4
        self.fin = (self.headerlenandflag >> 0) & 0x1
        self.syn = (self.headerlenandflag >> 1) & 0x1
        self.rst = (self.headerlenandflag >> 2) & 0x1
        self.psh = (self.headerlenandflag >> 3) & 0x1
        self.ack = (self.headerlenandflag >> 4) & 0x1
        self.ugr = (self.headerlenandflag >> 5) & 0x1

        #解析序号，确认序号，校验和，窗口大小
        self.sequnum = struct.unpack(">I", struct.pack("<I",self.sequnum))[0]
        self.acknowledgenum = struct.unpack(">I", struct.pack("<I",self.acknowledgenum))[0]
        self.windowsize = struct.unpack(">H", struct.pack("<H",self.windowsize))[0]
        self.checksum = struct.unpack(">H", struct.pack("<H",self.checksum))[0]

    def __str__(self):
        return "src port: {0}, dest port: {1}, ack: {2}, psh: {3}, rst: {4}, syn: {5}, fin: {6}".format(
            self.src_port, self.dest_port, self.ack, self.psh, self.rst, self.syn, self.fin)


if __name__ == '__main__':
    pc = pcap.pcap('bond0')
    # pc.setfilter('tcp port 80')
    for ptime, pdata in pc:
        eth = Ethernet(pdata[0:14])
        if eth.protocol == 'ARP':
            print eth
        elif eth.protocol == 'IP':
            ip_data = pdata[14:]
            ip_header = IP(ip_data)
            print ip_header
            if ip_header.protocol == 'TCP':
                tcp_data = ip_data[ip_header.ihl:]                
                tcp_header = TCP(tcp_data)
                print tcp_header