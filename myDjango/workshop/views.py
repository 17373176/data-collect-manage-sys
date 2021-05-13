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

from channels.layers import get_channel_layer
from django.shortcuts import render
from workshop.models import MachineInfo  # 导入models文件
from django.http import HttpResponse, JsonResponse
from workshop import msgResponse, dataBaseDao
from workshop.msgResponse import error_msg, success_msg
from dataAcquisition.ProducerThread import ProducerThread
from dataAcquisition.ConsumerThread import ConsumerThread
from dataAcquisition.multiProtocol import multi_acquisition, _float_round, data_to_x
from workshop.dataBaseDao import Redis_pool, insert_img
import redis
import logging


logger = logging.getLogger('log')


# Kafka生产者和消费者
kafka_producer = ProducerThread()
kafka_consumer = ConsumerThread()
try:
    # 守护主线程，主线程退出后子线程直接销毁
    kafka_producer.setDaemon(True)
    kafka_consumer.setDaemon(True)
    kafka_producer.start()
    kafka_consumer.start()
except Exception as e:
    print(e)
finally:
    kafka_producer.terminate()
    kafka_consumer.terminate()


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

        #info = MachineInfo(id='1', name='哈哈', value={'1': 2, '2': 'az'}, time='2020-01-02 12:20:20')
        #print("插入成功")
        #info.save()  # 后续考虑list列表批量添加，增加效率

        # print(MachineInfo.objects.filter(id='1')[0].value)  # filter获取查询集，用下标返回具体数据行，用.返回具体字段

        #redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        #redis_client.rpush("redis_list", json.dumps({'3':1, "2":"s"})) # 添加数据，list数据类型
        #a = redis_client.blpop("redis_list")[1]  # 获取并删除左边第一个，如果列表空则阻塞等待
        #print(a)
        #a = redis_client.blpop("redis_list")[1]  # 获取并删除左边第一个，如果列表空则阻塞等待
        #print(a)

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
        #machine = MachineInfo()
        #msg = machine.objects.filter()
        #return HttpResponse(msg + "<p>数据查找成功！</p>")


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
def data_send_all(request):
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
        redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        for i in range(100):
            redis_client.lpop("redis_list")  # 删除已访问数据前100个
        #message.append(redis_client.blpop("redis_list")[1])  # 获取并删除左边第一个, 如果列表空则阻塞
        return JsonResponse(success_msg(message))
    except Exception as e:
        return JsonResponse(error_msg(e))

