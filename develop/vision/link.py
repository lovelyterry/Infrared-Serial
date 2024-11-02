#!/usr/bin/env python3

# 该文件用于和热成像模块建立连接，获取热成像模块的原始数据
import serial
import re
import socket

from serial.tools import list_ports

# TCP连接方式
# TCP连接方式需要上位机和热成像模块处于同一局域网
# 如果是热成像模块开启热点，上位机去连接，那么默认的IP地址就是192.168.4.1
# 默认的端口为6666


class Tcp:
    def __init__(self, server):
        self.fd = None
        self.server = server

    def open(self):
        self.fd = socket.socket()
        self.fd.setblocking(1)
        self.fd.connect((self.server, 6666))

    def send(self, buffer):
        result = self.fd.send(buffer)
        if result == len(buffer):
            return result
        else:
            return None

    def recv(self):
        if self.fd is not None:
            buffer = self.fd.recv(65536)
            return buffer
        else:
            return None

    def close(self):
        if self.fd is not None:
            self.fd.close()


# 串口连接方式
# windows需要安装驱动，可以通过双击目录下的usbdriver.ps1完成安装
# 基于linux的系统自带驱动，不用安装
# 遍历USB设备，查找VID为303A，PID为1001的设备打开即可
# 波特率为921600，数据位8，无校验，停止位1
class Serial:
    def __init__(self):
        self.fd = None

    def open(self):
        ports = list(list_ports.comports())
        port = None
        for i in range(len(ports)):
            port = list(ports[i])
            if (re.match("USB VID:PID=303A:1001", port[2])):
                port = port[0]
                break
        if port == None:
            return None
        self.fd = serial.Serial(port, 921600, 8, 'N', 1, timeout=1)
        if self.fd.is_open:
            return self.fd
        else:
            return None

    def send(self, buffer):
        result = self.fd.write(buffer)
        if result == len(buffer):
            return result
        else:
            return None

    def recv(self):
        if self.fd.in_waiting:
            buffer = self.fd.read(self.fd.in_waiting)
            return buffer
        else:
            return None

    def close(self):
        if self.fd is not None and self.fd.is_open:
            self.fd.close()
