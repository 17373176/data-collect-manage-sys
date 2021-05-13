# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        ProducerThread.py
# Description:      kafka生产者线程
# Date:             2021/4/13
# License:          (C)Copyright 2021, Bob
# Function List:    将消息扔进kafka消息队列
#
#
# -----------------------------------------------------------------


import json
import sys
import time
from kafka import KafkaProducer
import threading


class ProducerThread(threading.Thread):
    """
    生产者线程类
    """
    running = False
    data = dict()
    kafka_server = "localhost:9092"
    topic = 'MQ'
    pro = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda m: json.dumps(m).encode('utf-8'))

    def __init__(self):  # 重写Thread类的构造函数
        super(ProducerThread, self).__init__()  # 调用父类构造函数

    def terminate(self):
        self.running = False

    def run(self):
            self.running = True
        #while self.running is True:
            if 'id' in self.data.keys():
                #print(self.data)
                self.pro.send(self.topic, json.dumps(self.data))
            # i = i + 1
            #self.running = False  # 等数据来再唤醒
            #time.sleep(0.1)




