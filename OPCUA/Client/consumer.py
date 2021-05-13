# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        consumer.py
# Description:      相关操作
# Date:             2021/4/13
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------

import threading
from kafka import  KafkaConsumer


class Con(threading.Thread):
    running = False

    def __init__(self):  # 重写Thread类的构造函数
        super(Con, self).__init__()  # 调用父类构造函数
        self.running = False

    def terminate(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running is True:
            kafka_server = "localhost:9092"
            topic = 'MQ'
            cus = KafkaConsumer(bootstrap_servers=["localhost:9092"], group_id="1", auto_offset_reset='earliest')
            cus.subscribe([topic])
            for i in cus:
                print(i.value)

