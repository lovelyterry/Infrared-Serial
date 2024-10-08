#!/usr/bin/env python3

import cv2
import numpy as np


class Image:
    # 根据所有像素中的最高温和最低温，将温度数据归一化为0~255
    def normalization(self, matrix):
        vMax = matrix.max()
        vMin = matrix.min()
        [rows, cols] = matrix.shape
        for i in range(rows):
            for j in range(cols):
                matrix[i][j] = (matrix[i][j] - vMin) / (vMax - vMin)
        imageGray = np.zeros(matrix.shape, dtype=np.uint8)
        for i in range(rows):
            for j in range(cols):
                imageGray[i][j] = 255 - matrix[i][j] * 255
        return imageGray

    def show(self, imageGray, style=cv2.COLORMAP_RAINBOW, algorithm=cv2.INTER_LANCZOS4, scale=10):
        [rows, cols] = imageGray.shape
        # 利用opencv的resize将32*32像素的数据插补为320*320
        imageResizeGray = cv2.resize(
            imageGray, (rows * scale, cols * scale), interpolation=algorithm)
        # 利用opencv的applyColorMap将温度数据转换为热图
        imageColor = cv2.applyColorMap(imageResizeGray, style)
        # 显示热图数据
        cv2.imshow("Infrared", imageColor)
        cv2.waitKey(10)
        if (cv2.getWindowProperty("Infrared", style) == 0):
            exit()
