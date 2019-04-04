import numpy as np
from skimage.feature import greycomatrix, greycoprops

# 特征类型参数
ENTROPY = 'entropy'
ENERGY = 'ASM'
CONTRAST = 'contrast'
HOMOGENEITY = 'homogeneity'

# 方向参数
A_0 = [0]
A_45 = [np.pi / 4]
A_90 = [np.pi / 2]
A_135 = [3 * np.pi / 4]

# 距离参数
DIS_1 = [1]
DIS_4 = [4]
DIS_10 = [10]


# 构建灰度共生矩阵
def build_glcm(image, distance, angles, levels):
    glcm = greycomatrix(image, distance, angles, levels, True, True)
    return glcm


# 获得熵
def get_entropy(g):
    p = g[:, :, 0, 0]
    p = p.ravel()
    result = -np.dot(np.log2(p + (p == 0)), p.ravel())
    return result


# 获得能量
def get_energy(g):
    result = greycoprops(g, ENERGY)
    return result[0][0]


# 获得对比度
def get_contrast(g):
    result = greycoprops(g, CONTRAST)
    return result[0][0]


# 获得逆差矩
def get_homogeneity(g):
    result = greycoprops(g, HOMOGENEITY)
    return result[0][0]


# 将图片灰度降低至0至gray_level-1
def gray_des(img, gray_level):
    max_gray = img.max() + 1
    height, width = img.shape
    for i in range(height):
        for j in range(width):
            img[i][j] = img[i][j] * gray_level // max_gray

    return img
