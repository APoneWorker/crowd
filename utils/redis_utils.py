import redis
import json
import cv2 as cv
import base64
import numpy as np

# 原始图片
ORIGIN_IMAGE = 'oi'
# 处理图片与结果
CONVERT_IMAGE = 'ci'


# 图片转base64
def image_to_base64(image_np):
    image = cv.imencode('.png', image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code


# base64转图片
def base64_to_image(base64_code):
    img_data = base64.b64decode(base64_code)
    img_array = np.frombuffer(img_data, np.uint8)
    img = cv.imdecode(img_array, cv.COLOR_BGR2GRAY)
    return img


# 将结果组合成列表，用于序列化，图片必须为转化为base64的图片
def convert(crowd_result, image_result):
    obj = {
        "result": crowd_result,
        "img": image_result,
    }
    return obj


# 图片缓存池，有两个队列分别为检测结果队列和原始图像队列
class ImageCachePool:

    def __init__(self, host, port, password=None):
        pool = redis.ConnectionPool(host=host, port=port, password=password, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)
        self.origin_list_max = 6 * 1
        self.result_list_max = 3

    # 插入结果，包含检测结果和处理后图像
    def set_result(self, crowd_result, image_result):
        image_result = image_to_base64(image_result)
        result = convert(crowd_result, image_result)
        json_result = json.dumps(result)
        response = self.r.lpush(CONVERT_IMAGE, json_result)
        if self.r.llen(CONVERT_IMAGE) > self.result_list_max:
            self.r.ltrim(CONVERT_IMAGE, 0, self.result_list_max - 1)
        return response

    # 插入原始图像
    def set_origin_image(self, origin_image):
        image_result = image_to_base64(origin_image)
        state = self.r.lpush(ORIGIN_IMAGE, image_result)
        if self.r.llen(ORIGIN_IMAGE) > self.origin_list_max:
            self.r.ltrim(ORIGIN_IMAGE, 0, self.origin_list_max - 1)
        return state

    # 获取结果，包含检测结果和处理后base64图像
    def get_result(self):
        result = self.r.lpop(CONVERT_IMAGE)
        return result

    # 获取原始图像,base64返回
    def get_origin_image(self):
        img = self.r.rpop(ORIGIN_IMAGE)
        return img

    # 获取结果，包含检测结果和处理后base64图像
    def view_result(self):
        result = self.r.lrange(CONVERT_IMAGE, -1, -1)
        if len(result) == 0:
            return None
        return result[0]

    # 查看先早原始图像，但不会弹出队列,base64返回
    def view_origin_image_to_web(self):
        # 该方法返回list,要注意
        img = self.r.lrange(ORIGIN_IMAGE, -1, -1)
        if len(img) == 0:
            return None
        return img[0]

    # 查看先早原始图像，但不会弹出队列,base64返回
    def view_origin_image_to_system(self):
        # 该方法返回list,要注意
        img = self.r.lrange(ORIGIN_IMAGE, -1, -1)
        if len(img) == 0:
            return None
        img = base64_to_image(img[0])
        return img
