# -*- coding: utf-8 -*-

import utils.redis_utils as redis
import crowd_implement.crowd_system as crowd_system
import config.config as config

pool = redis.ImageCachePool(config.server_redis_ip, config.redis_port, config.redis_password)

speed = crowd_system.speed

estimate_speed = crowd_system.estimate_speed


# 获取base64原始监控图像
def get_crowd_image():
    img = pool.view_origin_image_to_web()
    return img


# 获取base64处理图像和识别结果
def get_crowd_result():
    result = pool.view_result()
    return result
