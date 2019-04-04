from crowd_implement import backgroundCDM as bc
from crowd_implement.glcm_utils import *
import time
import threading
import utils.redis_utils as redis
import crowd_implement.naive_bayes_continuous as nbc
import random

speed = 1 / 24
estimate_speed = 1 / 12


# 背景更新
def update_background(pool):
    print('updating background......')
    build_count = 300
    images = []
    index = 0
    while index < build_count:
        time.sleep(speed)
        image = pool.view_origin_image_to_system()
        if image is not None:
            image = bc.images_pretreatment(image, 3)
            images.append(image)
            index += 1

    global background
    background = bc.build_background(images, build_count, bc.T_NORMAL)
    print('update successful......')


# 更新背景线程
def update_background_invoked(pool):
    # 随机时间进行背景更新
    update_background(pool)
    loop_time = random.randint(10, 15) * 60
    global scheduler
    scheduler = threading.Timer(loop_time, update_background_invoked, [pool])
    scheduler.start()


# 系统运行函数
def system_run():
    pool = redis.ImageCachePool('192.168.116.128', 6379)
    # 初始化背景建模
    update_background_invoked(pool)

    # 循环从缓存服务器中获取原始图像资源,但不会将图像弹出队列
    print('crowd estimate starting......')
    while True:
        current_image = pool.view_origin_image_to_system()
        if current_image is None:
            continue

        current_image = bc.images_pretreatment(current_image, 3)
        # 进行背景差分，获取人群前景图
        diff_img = bc.background_diff(background, current_image)

        # 创建模型
        model_nbc = nbc.NaiveBayesContinuous()
        model_nbc.load_model()

        # 降低灰度级
        c_img = gray_des(diff_img.copy(), 16)
        # 构建0度灰度共生矩阵
        glcm_0 = build_glcm(c_img, DIS_4, A_0, 16)
        # 构建45度灰度共生矩阵
        glcm_45 = build_glcm(c_img, DIS_4, A_45, 16)
        # 获得特征属性
        test = [get_energy(glcm_0), get_entropy(glcm_0), get_contrast(glcm_0), get_homogeneity(glcm_0),
                get_energy(glcm_45), get_entropy(glcm_45), get_contrast(glcm_45), get_homogeneity(glcm_45)]

        result, prob = model_nbc.predict(test)
        # 将图像和密度结果一同存入缓存服务器
        pool.set_result(result, diff_img)
        time.sleep(estimate_speed)
