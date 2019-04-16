# -*- coding: utf-8 -*-
# 系统以及redis配置文件

# 服务程序获取原始图片redis地址
server_redis_ip = '127.0.0.1'

# 捕获程序上传原始图片到redis地址
origin_redis_ip = '127.0.0.1'

# redis端口
redis_port = 6379

# redis密码
redis_password = '123456'

# 获取原始图片ws请求地址
origin_websocket_ip = '127.0.0.1'

# 获取原始图片ws请求端口
origin_websocket_port = 81

# 获取处理结果ws请求地址
result_websocket_ip = '127.0.0.1'

# 获取处理结果ws请求端口
result_websocket_port = 82

# 选择为读取本地图片集数据源地址
data = '../test1/all/'

# 本地图片数据源最大数
data_count_max = 10000
