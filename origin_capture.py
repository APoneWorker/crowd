# -*- coding: utf-8 -*-

import utils.redis_utils as redis
import threading
import time
import utils.video_stream as video_stream
import config.config as config

# 此程序适用于于本地以及远程
# 主要用于获取本地或远程的图像文件
speed = 1 / 24


# 原始图像线程
def origin_capture():
    video = video_stream.VideoStream(video_stream.DESKTOP, max_frame=config.data_count_max, url=config.data)
    image_pool = redis.ImageCachePool(config.origin_redis_ip, config.redis_port, config.redis_password)
    # 每秒24帧

    while True:
        time.sleep(speed)
        current_image = video.get_frame()
        if current_image is not None:
            image_pool.set_origin_image(current_image)


# 启动捕捉原始图像线程
def capture_start():
    print('origin image capture starting......')
    thread = threading.Thread(target=origin_capture)
    thread.start()
    print('origin image capture started......')


capture_start()
