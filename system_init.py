import crowd_implement.crowd_system as cc
import threading
import web_server


def system_init():
    print('init system......')
    cc.system_run()


thread = threading.Thread(target=system_init)
thread.start()
web_server.start()
