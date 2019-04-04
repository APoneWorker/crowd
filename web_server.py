from websocket_server import WebsocketServer
import service.crowd_service as  service
import time
import threading


# 新连接,同时开始传输原始监控画面
def new_origin_client(client, server):
    print('origin NO.(%d) observer has join' % client['id'])
    while True:
        time.sleep(service.speed)
        img = service.get_crowd_image()
        if img is not None:
            server.send_message(client, img)
        else:
            break


# 新连接，同时开始传输处理后的图像和识别结果
def new_result_client(client, server):
    print('result NO.(%d) observer has join' % client['id'])
    while True:
        time.sleep(service.estimate_speed)
        result = service.get_crowd_result()
        if result is not None:
            server.send_message(client, result)
        else:
            break


def client_left(client, server):
    print("NO.(%d) observer has left" % client['id'])


# origin
def origin_web():
    origin_server = WebsocketServer(81, "127.0.0.1")
    origin_server.set_fn_new_client(new_origin_client)
    origin_server.set_fn_client_left(client_left)
    origin_server.run_forever()


# result
def result_web():
    result_server = WebsocketServer(82, "127.0.0.1")
    result_server.set_fn_new_client(new_result_client)
    result_server.set_fn_client_left(client_left)
    result_server.run_forever()


def start():
    t1 = threading.Thread(target=origin_web)
    t2 = threading.Thread(target=result_web)
    t1.start()
    t2.start()
