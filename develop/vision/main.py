#!/usr/bin/env python3


from link import Serial, Tcp
from infrared import Infrared

infrared = Infrared()
serial = Serial()
tcp = Tcp("192.168.4.1")

# 这里默认使用串口进行连接
# 串口支持的命令有:
# 1. infrared\r\n         采集一帧的红外点阵数据
# 2. wifi on\r\n          开启wifi
# 3. wifi off\r\n         关闭wifi
# 4. emissivity\r\n       查询发射率
# 5. emissivity 0.xx\r\n  设置发射率，例如设置发射率为0.95：emissivity 0.95\r\n
# 6. calibrate\r\n        自动校准传感器
# 7. power reboot\r\n     重启模块
# 8. serial msgpack\r\n   切换到MSGPACK模式(切换到MSGPACK模式后无法切回其他模式)
# 10. serial prompt\r\n   切换到shell交互模式(默认)
# 11. serial common\r\n   切换到普通模式
port = serial

# TCP和UDP只支持MSGPACK模式

# 这是将python脚本编译成exe的命令，不用理会
"""
nuitka.bat --standalone --show-progress --enable-plugin=numpy --show-memory --onefile --output-dir=out main.py
"""

if __name__ == '__main__':
    # step 1: 打开连接
    port.open()
    try:
        # 串口需要先切换到MSGPACK模式，TCP和UDP默认使用MSGPACK模式，不用切换
        if (port == serial):
            port.send(b"serial msgpack\r\n")
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
