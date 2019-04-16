# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 13:39:04 2019

@author: APone
"""
# -*- coding: utf-8 -*-

import cv2 as cv
import numpy as np

T_NORMAL = 3

T_BC = 3


# 构造背景
def build_background(images, N, T):
    height = images[0].shape[0]
    width = images[0].shape[1]
    s = np.zeros([height, width, 2])

    for y in range(height):
        for x in range(width):
            flag = False
            start = 1
            end = 1
            for n in range(1, N - 1):
                d = abs(int(images[n][y, x]) - int(images[n - 1][y, x]))
                if d < T:
                    result = 0
                else:
                    result = d

                if result == 0 and flag is False:
                    start = n
                    flag = True
                elif result != 0 and flag is True:
                    end = n
                    flag = False
                    temp = int(s[y][x][1] - s[y][x][0])
                    if (end - start) > temp:
                        s[y][x][0] = start
                        s[y][x][1] = end

    background = images[0].copy()
    for y in range(height):
        for x in range(width):
            median = int((s[y, x][0] + s[y, x][1]) / 2)
            background[y][x] = images[median][y][x]

    return background


# 使用背景和图像进行差分提取前景图
def background_diff(background, images):
    c_frame = cv.absdiff(images, background)
    return c_frame


# 图像的预处理，使用中值滤波和加权平均灰度化
def images_pretreatment(images, T):
    images = cv.cvtColor(images, cv.COLOR_BGR2GRAY)
    images = cv.medianBlur(images, T)
    return images
