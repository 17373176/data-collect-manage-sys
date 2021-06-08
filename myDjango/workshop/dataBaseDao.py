# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        dataBaseDao.py
# Description:      写入Mysql数据库和Redis
# Date:             2021/4/13
# License:          (C)Copyright 2021, Bob
# Function List:    插入数据库表
#                   插入Redis
#
# -----------------------------------------------------------------


#from workshop.models import MachineInfo, ImgInfo
import json

import datetime
import redis
import influxdb


# Redis连接池
from workshop.defineConst import IMG_PATH
from workshop.models import ImgInfo, MachineInfo


Redis_pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)

# InfluxDB连接池
# Influx_pool = influxdb.InfluxDBClient('localhost', '8086', '')


def insert_machine(data):
    """
    数据存入local_db
    @param data:
    @return:
    """
    try:
        no = data['no']
        id = data['id']
        name = data['name']
        value = data['value']
        time = data['update_time']
        info = MachineInfo(no=no, id=id, name=name, value=value, update_time=time)
        info.save()  # 后续考虑list列表批量添加
        print('local_db数据添加成功！')
    except Exception as e:
        print(e)
        return e


def insert_img(data, request_read):
    """
    将图片存入local_db，redis
    @param data:
    @param request_read:
    @return:
    """
    from workshop.views import websocket_send_to_user

    tag = data['tag']
    id = data['id']
    time = data['update_time']  # 这里是datetime格式的日期
    name = data['name']
    value = data['value']
    img_data = data['data']
    # 存到数据库用'%Y/%m/%d %H:%M:%S'datetime格式
    # 存到本地文件夹，value文件名用'%Y-%m-%d_%H-%M-%S'字符串格式

    try:
        img = ImgInfo(id=id, tag=tag, name=name, vlue=value, update_time=time,
                      data=img_data)
        img.save()
        print('local_db图像路径添加成功！')
    except Exception as e:
        print(e)

    insert_redis(data)
    print('图像存储Redis成功！')

    # path+value: 文件路径+文件名
    with open(IMG_PATH[tag] + str(value), 'wb') as output:
        output.write(request_read)
    print('图像存储本地文件夹成功！')

    #websocket_send_to_user(data)


def insert_redis(data):
    """
    将数据存储到Redis缓存，采用list数据结构，前端不会主动查询，因此不会降低查询复杂度
    后端根据链表头部节点，依次把数据推给前端
    过期策略采用推送完成后删除，或设置过期时间10分钟
    @param data:
    @return:
    """
    try:
        redis_client = redis.Redis(connection_pool=Redis_pool)  # 连接池连接
        print('准备添加json格式数据到redis中')
        redis_client.rpush("redis_list", json.dumps(data))  # 添加数据，list数据类型，
        print('redis数据添加成功输出dict格式：')
        #print(json.loads(redis_client.blpop("redis_list")[1]))  # json.loads取出来即可
        print(json.loads(json.dumps(data)))
    except Exception as e:
        print(e)


def redis_set(key,value):
    '''
    将redis里的的key设为value
    @param key: 要设置的key值
    @param value: 要设置的value
    @return: true：成功，false：失败
    '''
    try:
        redis_client=redis.Redis(connection_pool=Redis_pool)
        redis_client.set(key,value)
        return True
    except Exception as e:
        print("redis_set:",e)
        return False


def redis_mset(data:dict):
    '''
    redis mset 封装
    @param data: 一个dict，所有要设的键值对
    @return: 成功返回true，否则返回false
    '''
    try:
        redis_client=redis.Redis(connection_pool=Redis_pool)
        redis_client.mset(data)
        return True
    except Exception as e:
        print("redis_mset:",e)
        return False
    pass


def redis_get(key,default):
    '''
    从redis读取key的值，若没有，用default代替
    @param key:
    @param default:
    @return:
    '''
    try:
        redis_client = redis.Redis(connection_pool=Redis_pool)
        result=redis_client.get(key)
        if result:
            return default
        else:
            return result
    except Exception as e:
        print("redis_get",e)
        return default
    pass


def redis_mget(keys:tuple,default:list):
    #print("mget data",keys)
    if len(keys)!=len(default):
        return None
    try:
        redis_client = redis.Redis(connection_pool=Redis_pool)
        result=redis_client.mget(keys)
        #print("result:",result)
        i=0
        while i<len(result):
            if not result[i]:
                result[i]=default[i]
            i+=1
            pass
        return result
    except Exception as e:
        print("redis_mget",e)
        return None
    pass

