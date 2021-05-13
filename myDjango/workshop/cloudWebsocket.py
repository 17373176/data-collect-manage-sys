# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        cloudWebsocket.py
# Description:      云端Websocket连接客户端
# Date:             2021/4/13
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------


import json
import websocket
import threading


def on_message(ws, message):   # 第一个参数必须传递
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws, data):
    def run():
        ws.send(json.dumps(data))
        # ws.close()  # 发送完毕, 可以不关闭

    t = threading.Thread(target=run)  # 启动线程执行run()函数发送数据
    t.setDaemon(True)
    t.start()

