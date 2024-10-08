#!/usr/bin/env python3

import image
import time

from link import Serial, Tcp
from infrared import Infrared

infrared = Infrared()
serial = Serial()
tcp = Tcp("192.168.4.1")
img = image.Image()

# 这里默认使用串口进行连接
port = serial

# 这是将python脚本编译成exe的命令，不用理会
"""
nuitka.bat --standalone --show-progress --enable-plugin=numpy --show-memory --onefile --output-dir=out main.py
"""

if __name__ == '__main__':
    # step 1: 打开连接
    port.open()
    try:
        # step 2: 向模块发送命令
        # 模块支持的命令有:
        # 1.   infrared\r\n          采集一帧的红外点阵数据
        # 2.   infrared off\r\n      关闭采集的红外点阵数据
        # 3.   infrared on\r\n       采集连续的红外点阵数据
        # 4.   temperature\r\n       获取一次中心温度
        # 5.   temperature off\r\n   关闭获取中心温度
        # 6.   temperature on\r\n    连续获取中心温度
        # 7.   wifi on\r\n           开启wifi
        # 8.   wifi off\r\n          关闭wifi
        # 9.   emissivity\r\n        查询发射率
        # 10.  emissivity 0.xx\r\n   设置发射率，例如设置发射率为0.95：emissivity 0.95\r\n
        # 11.  calibrate\r\n         自动校准传感器
        # 12.  power reboot\r\n      重启模块
        # 这里开启连续采集模式
        port.send(b"infrared on\r\n")
        while True:
            # step 3: 从模块中获取红外数据帧
            frame = infrared.parse(port.recv())
            # step 4: 将数据温度从数据帧中解析出来，转换为矩阵的形式
            tempMatrix = infrared.calculateCelsius(frame)
            if (tempMatrix is None):
                continue
            # step 5: 将温度打印出来
            infrared.printTemp(tempMatrix)
            # step 6: 将温度数据渲染成热图
            img.show(img.normalization(tempMatrix))
    except Exception as e:
        print(e)
    port.close()
