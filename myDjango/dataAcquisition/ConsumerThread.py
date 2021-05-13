# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        ConsumerThread.py
# Description:      相关操作
# Date:             2021/4/13
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------
import json
import threading
import time

from kafka import KafkaConsumer
from dataAcquisition.multiProtocol import data_store_db


class ConsumerThread(threading.Thread):
    """
    消费者线程类
    """
    running = False

    def __init__(self):  # 重写Thread类的构造函数
        super(ConsumerThread, self).__init__()  # 调用父类构造函数

    def terminate(self):
        self.running = False

    def run(self):
        kafka_server = "localhost:9092"
        topic = 'MQ'
        self.running = True
        consumer = KafkaConsumer(bootstrap_servers=kafka_server, auto_offset_reset='earliest')
        while self.running is True:
            consumer.subscribe([topic])
            if consumer:
                for data in consumer:
                    data = eval(json.loads(str(data.value, 'utf-8')))  # 读取为字典形式的数据
                    #print(data)
                    if 'id' in data.keys():
                        data_store_db(data)  # 拉取数据存储到本地数据库
                    time.sleep(0.001)



