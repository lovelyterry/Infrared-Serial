#!/usr/bin/env python3

import struct
import numpy as np


class Infrared:
    def __init__(self):
        self.cache = bytearray()

    def calculateCelsius(self, frame):
        if (frame is None):
            return None
        tempMatrix = np.zeros([32, 32], dtype=float)
        for i in range(int(len(frame) / 2)):
            temp = struct.unpack("H", frame[i*2:i*2+2])[0]
            y = int(i / 32)
            x = int(i % 32)
            # 解析原始数据为摄氏度，原始数据为开尔文温度，量纲为0.1，这里转换为摄氏度：除以10得到开尔文温度，再减去273.15(绝对零度)
            tempMatrix[y][x] = (float)(temp) / 10.0 - 273.15
        return tempMatrix

    def printTemp(self, tempMatrix):
        if (tempMatrix is None):
            return None
        print("\n\n")
        print('\n'.join([' '.join(['{:.1f}'.format(item)
                                   for item in row]) for row in tempMatrix]))

    def parse(self, buffer):
        # 原始的温度数据为二进制形式，类型为 uint16[1024],并以连续的两个\r\n结尾，用于作为分界
        # uint16的数据为该像素点的开尔文温度*10
        if (buffer is None):
            return None
        # 将串口收到的数据放置于缓存中
        self.cache.extend(buffer)
        token = b'\r\n\r\n'
        # 寻找上一帧数据的结尾
        indexTokenStart = self.cache.find(token)
        # 寻找这一次帧数据的结尾
        indexTokenEnd = self.cache.find(token, indexTokenStart + len(token))
        # 定位这一次数据帧的起始
        startOfFrame = indexTokenStart + len(token)
        # 得到数据帧长度
        frameLength = indexTokenEnd - startOfFrame
        if (indexTokenStart >= 0 and indexTokenEnd > indexTokenStart and frameLength == 2048):
            frame = self.cache[startOfFrame:indexTokenEnd]
            self.cache = self.cache[indexTokenEnd:]
            # 得到数据帧切片
            return frame
        # 缓存溢出，清空
        elif (len(self.cache) > 4096):
            self.cache = bytearray()
        return None
