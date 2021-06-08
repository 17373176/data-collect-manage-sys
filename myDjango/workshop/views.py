# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        views.py
# Description:      数据库相关操作，增删查改，将数据格式化后存储，实现前后端交互
# Function List:    views里可以定义全局变量，实例化对象，会自动按顺序调用的
#
#
# -----------------------------------------------------------------


# Create your views here.
import datetime
import json
import sys
import time
import _thread

from channels.layers import get_channel_layer
from django.shortcuts import render
from workshop.models import MachineInfo, StaticInfo  # 导入models文件
from django.http import HttpResponse, JsonResponse
from workshop import msgResponse, dataBaseDao
from workshop.msgResponse import error_msg, success_msg
from dataAcquisition.ProducerThread import ProducerThread
from dataAcquisition.ConsumerThread import ConsumerThread
from dataAcquisition.multiProtocol import multi_acquisition, _float_round, data_to_x
from workshop.dataBaseDao import Redis_pool, insert_img
import redis
import logging
from asgiref.sync import async_to_sync

import paho.mqtt.client as mqtt

HOST = "115.236.52.123"
PORT = 8883
User = "ce060bd8-2430-4d11-803c-ec9a7be8dc8e"
Password = "123456"
mqttclient = mqtt.Client()
# robot1 = {
#     "robotId": "0b87fab2-9df5-4327-99d3-39ef69c1894e",
#     "timestamp": int(time.time() * 1000),
#     "fCurJoint1": 0,
#     "fCurJoint2": 0,
#     "fCurJoint3": 0,
#     "fCurJoint4": 0,
#     "fCurJoint5": 0,
#     "fCurJoint6": 0,
#     "fAxisTorque1": 0.0,
#     "fAxisTorque2": 0.0,
#     "fAxisTorque3": 0.0,
#     "fAxisTorque4": 0.0,
#     "fAxisTorque5": 0.0,
#     "fAxisTorque6": 0.0,
#     "fAxisSpeed1": 0.0,
#     "fAxisSpeed2": 0.0,
#     "fAxisSpeed3": 0.0,
#     "fAxisSpeed4": 0.0,
#     "fAxisSpeed5": 0.0,
#     "fAxisSpeed6": 0.0,
# }
# robot2 = {
#     "robotId": "786f8c2a-15bd-4550-bdbd-96b2dba0a129",
#     "timestamp": int(time.time() * 1000),
#     "fCurJoint1": 0,
#     "fCurJoint2": 0,
#     "fCurJoint3": 0,
#     "fCurJoint4": 0,
#     "fCurJoint5": 0,
#     "fCurJoint6": 0,
#     "fAxisTorque1": 0.0,
#     "fAxisTorque2": 0.0,
#     "fAxisTorque3": 0.0,
#     "fAxisTorque4": 0.0,
#     "fAxisTorque5": 0.0,
#     "fAxisTorque6": 0.0,
#     "fAxisSpeed1": 0.0,
#     "fAxisSpeed2": 0.0,
#     "fAxisSpeed3": 0.0,
#     "fAxisSpeed4": 0.0,
#     "fAxisSpeed5": 0.0,
#     "fAxisSpeed6": 0.0,
# }

logger = logging.getLogger('log')


######################## [2021/5/15] 王广建：读取redis并将数据用mqtt发送到云端broker#############################
def send_state():
    while True:
        #redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        # rebot1和rebot2的键值列表
        redis_key1=["ro1_fCurJoint1","ro1_fCurJoint2","ro1_fCurJoint3","ro1_fCurJoint4",\
                "ro1_fAxisTorque1","ro1_fAxisTorque2","ro1_fAxisTorque3","ro1_fAxisTorque4"]
        redis_key2=["ro2_fCurJoint1", "ro2_fCurJoint2", "ro2_fCurJoint3", "ro2_fCurJoint4", \
                "ro2_fAxisTorque1", "ro2_fAxisTorque2", "ro2_fAxisTorque3","ro2_fAxisTorque4"]
        robot_key=["fCurJoint1","fCurJoint2","fCurJoint3","fCurJoint4",\
                "fAxisTorque1","fAxisTorque2","fAxisTorque3","fAxisTorque4"]
        redis_result1=dataBaseDao.redis_mget(redis_key1,[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])
        redis_result2 = dataBaseDao.redis_mget(redis_key2,[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        robot1 = {
            "robotId": "0b87fab2-9df5-4327-99d3-39ef69c1894e",
            "timestamp": int(time.time() * 1000),
            "fCurJoint1": 0,
            "fCurJoint2": 0,
            "fCurJoint3": 0,
            "fCurJoint4": 0,
            "fCurJoint5": 0,
            "fCurJoint6": 0,
            "fAxisTorque1": 0.0,
            "fAxisTorque2": 0.0,
            "fAxisTorque3": 0.0,
            "fAxisTorque4": 0.0,
            "fAxisTorque5": 0.0,
            "fAxisTorque6": 0.0,
            "fAxisSpeed1": 0.0,
            "fAxisSpeed2": 0.0,
            "fAxisSpeed3": 0.0,
            "fAxisSpeed4": 0.0,
            "fAxisSpeed5": 0.0,
            "fAxisSpeed6": 0.0,
        }
        robot2 = {
            "robotId": "786f8c2a-15bd-4550-bdbd-96b2dba0a129",
            "timestamp": int(time.time() * 1000),
            "fCurJoint1": 0,
            "fCurJoint2": 0,
            "fCurJoint3": 0,
            "fCurJoint4": 0,
            "fCurJoint5": 0,
            "fCurJoint6": 0,
            "fAxisTorque1": 0.0,
            "fAxisTorque2": 0.0,
            "fAxisTorque3": 0.0,
            "fAxisTorque4": 0.0,
            "fAxisTorque5": 0.0,
            "fAxisTorque6": 0.0,
            "fAxisSpeed1": 0.0,
            "fAxisSpeed2": 0.0,
            "fAxisSpeed3": 0.0,
            "fAxisSpeed4": 0.0,
            "fAxisSpeed5": 0.0,
            "fAxisSpeed6": 0.0,
        }
        # getdata = {'ro1': False, 'ro2': False, 'ro1Tor1': False, 'ro1Tor2': False, 'ro1Tor3': False, 'ro1Tor4': False,
        #            'ro2Tor': False}
        # for msg in messages:
        #     msg = json.loads(msg)
        #     if msg['id'] == '2' and not getdata['ro1']:
        #         robot1['fCurJoint1'] = msg['value']['J1']
        #         robot1['fCurJoint2'] = msg['value']['J2']
        #         robot1['fCurJoint3'] = msg['value']['J3']
        #         robot1['fCurJoint4'] = msg['value']['J4']
        #         getdata['ro1'] = True
        #     elif msg['id'] == '9':
        #         if 'J1' in msg['value'] and not getdata['ro1Tor1']:
        #             robot1['fAxisTorque1'] = msg['value']['J1']
        #             getdata['ro1Tor1'] = True
        #         if 'J2' in msg['value'] and not getdata['ro1Tor2']:
        #             robot1['fAxisTorque2'] = msg['value']['J2']
        #             getdata['ro1Tor2'] = True
        #         if 'J3' in msg['value'] and not getdata['ro1Tor3']:
        #             robot1['fAxisTorque3'] = msg['value']['J3']
        #             getdata['ro1Tor3'] = True
        #         if 'J4' in msg['value'] and not getdata['ro1Tor4']:
        #             robot1['fAxisTorque4'] = msg['value']['J4']
        #             getdata['ro1Tor4'] = True
        #     elif msg['id'] == '16' and not getdata['ro2']:
        #         robot2['fCurJoint1'] = msg['value']['J1']
        #         robot2['fCurJoint2'] = msg['value']['J2']
        #         robot2['fCurJoint3'] = msg['value']['J3']
        #         robot2['fCurJoint4'] = msg['value']['J4']
        #         getdata['ro2'] = True
        #     elif msg['id'] == '17' and not getdata['ro2Tor']:
        #         robot2['fAxisTorque1'] = msg['value']['J1']
        #         robot2['fAxisTorque2'] = msg['value']['J2']
        #         robot2['fAxisTorque3'] = msg['value']['J3']
        #         robot2['fAxisTorque4'] = msg['value']['J4']
        #         getdata['ro2Tor'] = True
        #     # 判断是否都找到了
        #     if getdata['ro1'] and getdata['ro2'] and getdata['ro2Tor'] and getdata['ro1Tor1'] and getdata['ro1Tor2'] and \
        #             getdata['ro1Tor3'] and getdata['ro1Tor4']:
        #         break
        index=0
        while index<len(redis_key1):#给robot1赋值
            robot1[robot_key[index]]=redis_result1[index]
            index+=1

        index=0
        while index<len(redis_key1):#给robot1赋值
            robot2[robot_key[index]]=redis_result2[index]
            index+=1
        param1 = json.dumps(robot1)
        param2 = json.dumps(robot2)
        mqttclient.publish("ce060bd8-2430-4d11-803c-ec9a7be8dc8e", payload=param1, qos=0)
        mqttclient.publish("ce060bd8-2430-4d11-803c-ec9a7be8dc8e", payload=param2, qos=0)
        # print("发送成功：", robot1,"\n", robot2)
        time.sleep(0.1)
    pass


def on_connect(client, userdata, flags, rc):
    '''
    订阅信息
    :param client: 链接
    :param userdata:
    :param flags:
    :param rc:
    :return:
    '''
    print('---链接-----------------------------')
    print(f'Connected with result code {rc}')
    print("---链接结束-------------")
    pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f'Unexpeced disconnection {rc}--disconnect')
        pass
    pass


def on_message(client, userdata, msg):
    print("--------------get message--------------------")
    print(msg.payload.decode("utf-8"))
    print("---------------------------------------------")
    pass


def send_to_broker(HOST, PORT, Username, Password):
    '''
    start the thread that send the state of robot to mqtt broker
    :param HOST: IP of the mqtt broker
    :param PORT: Port of the broker
    :param username: client name
    :param password: client pw
    :return: nothing return
    '''
    mqttclient.on_connect = on_connect
    mqttclient.on_disconnect = on_disconnect
    mqttclient.on_message = on_message
    mqttclient.username_pw_set(Username, Password)
    mqttclient.connect(HOST, PORT, 60)
    mqttclient.subscribe("ce060bd8-2430-4d11-803c-ec9a7be8dc8e")
    send_state()
    mqttclient.loop_forever()


###########################################################################################################


# Kafka生产者和消费者
'''
kafka_producer = ProducerThread()
kafka_consumer = ConsumerThread()'''

try:
    _thread.start_new_thread(send_to_broker, (HOST, PORT, User, Password))
except Exception as excep:
    print("start_new_thread", excep)


def index(request):
    return render(request, 'index.html', {})


def room(request):
    return render(request, 'room.html', {
    })


def websocket_send_to_user(data):
    """
    发送数据给前端
    @param data:
    @return:
    """
    # 通过get_channel_layer()获取channel层
    channel_layer = get_channel_layer()
    if channel_layer is not None:
        # "type"字段必须，且值为WorkshopConsumer内对应处理函数的函数名
        async_to_sync(channel_layer.group_send)(
            'group_factory',
            {
                "type": "workshop_message",
                "message": data
            }
        )


def test(request):
    try:

        # info = MachineInfo(id='1', name='哈哈', value={'1': 2, '2': 'az'}, time='2020-01-02 12:20:20')
        # print("插入成功")
        # info.save()  # 后续考虑list列表批量添加，增加效率

        # print(MachineInfo.objects.filter(id='1')[0].value)  # filter获取查询集，用下标返回具体数据行，用.返回具体字段

        # redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        # redis_client.rpush("redis_list", json.dumps({'3':1, "2":"s"})) # 添加数据，list数据类型
        # a = redis_client.blpop("redis_list")[1]  # 获取并删除左边第一个，如果列表空则阻塞等待
        # print(a)
        # a = redis_client.blpop("redis_list")[1]  # 获取并删除左边第一个，如果列表空则阻塞等待
        # print(a)

        # 守护主线程，主线程退出后子线程直接销毁
        '''kafka_producer.setDaemon(True)
        kafka_consumer.setDaemon(True)
        kafka_producer.start()
        kafka_consumer.start()
        for i in range(1):
            time.sleep(1)
            kafka_producer.data = {'id': '10', '10': {'J1': '0'}, 'update_time': '2021/5/7 20:45'}
            kafka_producer.run()  # 数据来，唤醒生产者
        time.sleep(3)
        kafka_producer.terminate()
        kafka_consumer.terminate()'''
        # machine = MachineInfo()
        # msg = machine.objects.filter()
        # return HttpResponse(msg + "<p>数据查找成功！</p>")
        '''try:
            # 守护主线程，主线程退出后子线程直接销毁
            kafka_producer.setDaemon(True)
            kafka_consumer.setDaemon(True)
            kafka_producer.start()
            kafka_consumer.start()
            time.sleep(10)
        except Exception as e:
            print(e)
        finally:
            kafka_producer.terminate()
            kafka_consumer.terminate()'''

        return HttpResponse(1)
    except Exception as e:
        print(e)
        return HttpResponse("异常")


def add_static_info(data):
    """
    增加机器静态信息
    @param data:
    @return:
    """
    try:
        no = data['no']
        id = data['id']
        name = data['name']
        time = data['update_time']
        info = StaticInfo(no=no, id=id, name=name, update_time=time)
        info.save()  # 后续考虑list列表批量添加
        print('local_db数据添加成功！')
    except Exception as e:
        print(e)
        return e


# --------------与前端交互-------------- #
def data_send_all():
    """
    给前端传的数据
    """
    try:
        redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        data = redis_client.blpop("redis_list")[1]  # 获取并删除左边第一个, 如果列表空则阻塞
        websocket_send_to_user(data)
        return JsonResponse(success_msg(data))  # 通过http的请求，在响应的时候附带数据
    except Exception as e:
        return JsonResponse(error_msg(e))


def query_workshop1(request):
    """
    前端查询本地数据库，获取机械臂1信息
    @param request:
    @return:
    """
    # # 找出最近5分钟的time > now() - 5m, 时间减去5，5分钟内的数据
    now = (datetime.datetime.now() + datetime.timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
    info = MachineInfo.objects.filter(Q(id='2') & Q(time__gt=now))[0].value  # filter获取查询集，用下标返回具体数据行，用.返回具体字段
    robot = {json.dumps(info)}
    return JsonResponse(success_msg(robot))


def query_workshop2(request):
    """
    前端查询本地数据库，获取机械臂2信息
    @param request:
    @return:
    """
    # 找出最近5分钟的time > now() - 5m
    now = (datetime.datetime.now() + datetime.timedelta(minutes=-5)).strftime("%Y-%m-%d %H:%M:%S")
    info = MachineInfo.objects.filter(Q(id='16') & Q(time__gt=now))[0].value  # filter获取查询集，用下标返回具体数据行，用.返回具体字段
    robotAll = []
    pos = []
    target = []
    for item in info.get_points():
        robotAll.append(literal_eval(item['value']))
        # robotAll = literal_eval(item['value'])
    if len(robotAll) == 1:
        pos.append(_float_round(robotAll[0]["J1"]))
        pos.append(_float_round(robotAll[0]["J2"]))
        pos.append(_float_round(robotAll[0]["J3"]))
        pos.append(_float_round(robotAll[0]["J4"]))

    else:
        x = robotAll[len(robotAll) - 2]
        pos.append(_float_round(x["J1"]))
        pos.append(_float_round(x["J2"]))
        pos.append(_float_round(x["J3"]))
        pos.append(_float_round(x["J4"]))
        target.append(_float_round(robotAll[-1]["J1"]))
        target.append(_float_round(robotAll[-1]["J2"]))
        target.append(_float_round(robotAll[-1]["J3"]))
        target.append(_float_round(robotAll[-1]["J4"]))
    robot = {"pos": pos, "target": target}
    return JsonResponse(success_msg(robot))


def data_get_all(request):
    """
    前端查询本地缓存，获取所有信息
    @param request:
    @return:
    """
    try:
        redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        # 以list的形式添加，每次取100的数据
        message = redis_client.lrange("redis_list", 0, 99)  # 区间[0, 99]的数据
        # redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        for i in range(100):
            redis_client.lpop("redis_list")  # 删除已访问数据前100个
        # message.append(redis_client.blpop("redis_list")[1])  # 获取并删除左边第一个, 如果列表空则阻塞
        # print(message)
        return JsonResponse(success_msg(message))
    except Exception as e:
        return JsonResponse(error_msg(e))
