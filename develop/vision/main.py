#!/usr/bin/env python3


from link import Serial, Tcp
from infrared import Infrared

infrared = Infrared()
serial = Serial()
tcp = Tcp("192.168.4.1")


port = serial

# 这是将python脚本编译成exe的命令，不用理会
"""
nuitka.bat --standalone --show-progress --enable-plugin=numpy --show-memory --onefile --output-dir=out main.py
"""

if __name__ == '__main__':
    # step 1: 打开连接
    port.open()
    try:
        while True:
            # step 3: 从模块中获取红外数据帧
            data = port.recv()
            # step 4: 从模块中解析数据
            tempMatrix = infrared.parse(data)
            if (tempMatrix is None):
                continue
            # step 5: 将温度数据渲染成热图
            infrared.show(infrared.normalization(tempMatrix))
    except Exception as e:
        print(e)
    port.close()
