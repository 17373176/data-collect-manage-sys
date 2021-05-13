# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        kaf.py
# Description:      相关操作
# Date:             2021/4/13
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------


import datetime
import json
import time
from kafka import KafkaProducer
import threading
from Client.consumer import Con
import redis


class Pro(threading.Thread):
    """
    生产者线程
    """
    running = False

    def __init__(self):
        super(Pro, self).__init__()  # 调用父类构造函数
        self.running = False

    def terminate(self):
        self.running = False

    def run(self):
        self.running = True
        while self.running is True:
            kafka_server = "localhost:9092"
            topic = 'MQ'
            pro = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda m: json.dumps(m).encode())
            for i in range(100):
                data = {'num': i, 'ts': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                pro.send(topic, data)
                time.sleep(1)


if __name__ == "__main__":
    '''pro = Pro()
    con = Con()

    pro.start()
    con.start()

    #pro.join()
    #con.join()
    print ("hhhhhh")
    '''


