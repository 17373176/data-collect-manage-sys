# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        multiProtocol.py
# Description:      集成多协议数据采集接口
# Date:             2021/3/11
# License:          (C)Copyright 2021, Bob
# Function List:    三种协议接口的实现
#                   将数据放入kafka消息队列
#                   创建kafka生产者，消费者对象，保持一直开启
#                   消费者将数据写入数据库和Redis
# -----------------------------------------------------------------
import datetime
import json
import time
import websocket
from django.http import JsonResponse

from dataAcquisition.client import data_acquisition
from workshop import dataBaseDao
from workshop import views
from workshop.cloudWebsocket import on_open, on_message, on_error, on_close
from workshop.dataBaseDao import insert_img
from workshop.defineConst import IMG_TAG_ID, IMG_TAG_NAME, IMG_TAG, ID_TO_NO, MACHINE_ID_NAME, RESULT_ID_VALUE, \
    ID_QUALIFIED_VALUE, ACTION_ID_VALUE
from workshop.msgResponse import success_msg, error_msg
# from workshop.views import logger


def multi_acquisition(request, protocol):
    """
    集成多协议，根据protocol字段选取具体的传输协议，
    创建kafka生产者和消费者对象，生产者将数据扔进kafka，消费者从kafka队列拉取消息
    @param request: 服务器传输请求
    @param protocol: 服务器所选协议
    @return:
    """
    data = {}

    if protocol == 'opcua':
        data = data_acquisition(request)
    elif protocol == 'mqtt':
        data = data_mqtt(request)
    elif protocol == 'webSocket':
        data = data_webSocket(request)
    else:
        JsonResponse(error_msg("不支持的协议"))
    views.kafka_producer.data = data
    views.kafka_producer.running = True  # 将接收到的数据写入消息队列


def data_mqtt(request):
    """
    通过MQTT协议接收数据
    @param request:
    @return:  data
    """
    receive = request.POST.get('data')
    if not receive:
        return JsonResponse(error_msg('data is required'))
    try:
        data = json.loads(receive)
        print('MQTT协议传输正常')
    except Exception as e:
        logger.error("Error in insert_data_set: %s" % e)
        raise JsonResponse(error_msg('数据不是json格式'))
    return data


def data_webSocket(request):
    """
    通过webSocket协议接收数据
    @param request:
    @return:  data
    """
    receive = request.POST.get('data')
    if not receive:
        return JsonResponse(error_msg('data is required'))
    try:
        data = json.loads(receive)
        print('webSocket协议传输正常')
    except Exception as e:
        logger.error("Error in insert_data_set: %s" % e)
        raise JsonResponse(error_msg('数据不是json格式'))
    return data


def insert_data_set(request):
    """
    从边缘端接收数据，根据http传输
    @param request: http请求
    @return: JsonResponse
    """
    receive = request.POST.get('data')
    #print(receive)
    if not receive:  # 空请求
        return JsonResponse(error_msg('data is required'))

    try:
        data = json.loads(receive)
    except Exception as e:
        if 'Expecting value' in Exception:
            raise Exception
        logger.error("Error in insert_data_set: %s" % e)
        raise JsonResponse(error_msg('数据不是json格式'))
    if 'id' in data.keys():
        #views.kafka_producer.data = data  # 将接收到的数据写入消息队列
        #views.kafka_producer.run()  # 发送到队列

        '''if data['id'] == '17' or data['id'] == '15' or data['id'] == '11' or data['id'] == '12' or data['id'] == '12_1' \
                or data['id'] == '12_2' or data['id'] == '12_3' or data['id'] == '13' or data['id'] == '14' or data['id'] == '16':'''

        #if data['id'] == '21_1' or data['id'] == '21_2' or data['id'] == '21_3' or data['id'] == '21_4' or data['id'] == '21_5' or\
            #data['id'] == '21_6' or data['id'] == '21_7' or data['id'] == '21_8' or data['id'] == '21_9':
        # if data['id'] == '22_1' or data['id'] == '22_2' or data['id'] == '22_3' or data['id'] == '22_4' or data[
        #     'id'] == '22_5' or \
        #         data['id'] == '22_6' or data['id'] == '22_7' or data['id'] == '22_8' or data['id'] == '22_9':
        #if data['id'] == '14' or data['id'] == '11' or data['id'] == '13' or data['id'] == '15':
        # if data['id'] == '31' or data['id'] == '32' or data['id'] == '33' or data['id'] == '34' or data['id'] == '35' \
        #         or data['id'] == '36' or data['id'] == '37' or data['id'] == '38':
        data_store_db(data)
    return JsonResponse(success_msg("数据接收成功"))


def data_store_db(data):
    """
    将数据写入数据库local_db，Redis
    @param data:
    @return:
    """
    from workshop.views import websocket_send_to_user
    # 数据预处理
    data = data_to_x(data)
    #print(data)
    id = data['id']
    if id == '2':  # 保留两位小数
        data['value']['J1'] = _float_round(data['value']['J1'])
        data['value']['J2'] = _float_round(data['value']['J2'])
        data['value']['J3'] = _float_round(data['value']['J3'])
        data['value']['J4'] = _float_round(data['value']['J4'])
    elif id == '16':  # 角度转换
        data['value']['J1'] = J12_num(data['value']['J1'])
        data['value']['J2'] = J12_num(data['value']['J2'])
        data['value']['J3'] = J3_num(data['value']['J3'])
        data['value']['J4'] = J4_num(data['value']['J4'])

    #print(data)

    redis_set_data={}
    if data['id'] == '2' :
        redis_set_data['ro1_fCurJoint1'] = data['value']['J1']
        redis_set_data['ro1_fCurJoint2'] = data['value']['J2']
        redis_set_data['ro1_fCurJoint3'] = '-'+data['value']['J3']
        redis_set_data['ro1_fCurJoint4'] = data['value']['J4']
        dataBaseDao.redis_mset(redis_set_data)
    elif data['id'] == '9':
        #print(data)
        if 'J1' in data['value']:
            redis_set_data['ro1_fAxisTorque1'] = data['value']['J1']
        if 'J2' in data['value']:
            redis_set_data['ro1_fAxisTorque2'] = data['value']['J2']
        if 'J3' in data['value'] :
            redis_set_data['ro1_fAxisTorque3'] = data['value']['J3']
        if 'J4' in data['value'] :
            redis_set_data['ro1_fAxisTorque4'] = data['value']['J4']
        dataBaseDao.redis_mset(redis_set_data)
    elif data['id'] == '16' :
        redis_set_data['ro2_fCurJoint1'] = data['value']['J1']
        redis_set_data['ro2_fCurJoint2'] = data['value']['J2']
        redis_set_data['ro2_fCurJoint3'] = data['value']['J3']
        redis_set_data['ro2_fCurJoint4'] = data['value']['J4']
        dataBaseDao.redis_mset(redis_set_data)
    elif data['id'] == '17':
        redis_set_data['ro2_fAxisTorque1'] = data['value']['J1']
        redis_set_data['ro2_fAxisTorque2'] = data['value']['J2']
        redis_set_data['ro2_fAxisTorque3'] = data['value']['J3']
        redis_set_data['ro2_fAxisTorque4'] = data['value']['J4']
        dataBaseDao.redis_mset(redis_set_data)
    #print(redis_set_data)

    dataBaseDao.insert_redis(data)
    #dataBaseDao.insert_machine(data)

    # 发送给前端
    websocket_send_to_user(data)
    # data_upload_cloud(data)


def img_upload(request, tag):
    """
    图片数据的接收
    @param request:
    @param tag:
    @return:
    """
    request_read = request.read()
    imgdata = img_data(request_read, tag)  # 图片数据预处理
    insert_img(imgdata, request_read)  # 图片信息存入数据库和缓存，再把图片数据存入本地
    return JsonResponse(success_msg("图片接收成功"))


def file_upload_L1(request):
    """
    从边缘端接收图片文件
    @param request:
    @return:
    """
    return img_upload(request, IMG_TAG[1])


def file_upload_L2(request):
    return img_upload(request, IMG_TAG[2])


def file_upload_reg(request):
    return img_upload(request, IMG_TAG[3])


def file_upload_action(request):
    return img_upload(request, IMG_TAG[4])


def file_upload_result(request):
    return img_upload(request, IMG_TAG[5])


# 云端webSocket的url = ws:/data/cloud
cloud_url = "115.236.52.123"


def data_upload_cloud(data):
    """
    数据上传到杭州私有云服务器，通过webSocket连接
    @param data:
    @return:
    """
    try:
        websocket.enableTrace(True)  # True 默认在控制台打印连接和信息发送接收情况
        # 连接后自动调用发送函数，主动发送数据给云端
        ws = websocket.WebSocketApp(cloud_url)
        ws.on_open = on_open(ws, data)
        ws.on_message = on_message
        ws.on_error = on_error
        ws.on_close = on_close
        ws.run_forever()  # 开启长连接
        print('数据上传到云服务器成功!')
    # except KeyboardInterrupt: # 会被ws内部捕捉
    except Exception as e:  # ws 断开 或者psycopg2.OperationalError
        logger.warning("ws 断开 或者psycopg2.OperationalError, {}: {}".format(type(e), e))


# ----------数据预处理---------- #
def _float_round(data):
    if data.strip() != 0 and data.strip() != '':
        return str(round(float(data.strip()), 2))


def J12_num(data):
    x = float(data.strip())
    num1 = round(x / (80 * 100000) * 360, 2)
    return str(num1)


def J3_num(data):
    x = float(data.strip())
    num1 = round(x / 100000 * 8, 2)
    return str(num1)


def J4_num(data):
    x = float(data.strip())
    num1 = round(x / (51 * 100000) * 360, 2)
    return str(num1)


def data_to_x(pre_data):
    """
    格式化数据
    @param data:
    @return:
    """
    id = pre_data['id']
    data = {}
    ##############王广建：时间转换，考虑多种时间精度########################
    '''原代码
    # 时间从str字符串转化为dateTime格式
    str_time = time.strptime(pre_data["update_time"], '%Y/%m/%d %H:%M')
    year, month, day, hour, min = str_time[:5]
    time_temp = datetime.datetime(year, month, day, hour, min).strftime('%Y/%m/%d %H:%M:%S')
    # 将str转化为datetime
    '''
    strip_time = pre_data['update_time'].strip()
    #print("strip time:", strip_time)
    year, mounth, day, hour, min, sec = 0, 0, 0, 0, 0, 0
    #print(pre_data['update_time'])
    if strip_time.count(':') >= 2:
        str_time = time.strptime(pre_data["update_time"], '%y/%m/%d %H:%M:%S')
        year, month, day, hour, min, sec = str_time[:6]
    else:
        str_time = time.strptime(pre_data["update_time"], '%Y/%m/%d %H:%M')
        year, month, day, hour, min = str_time[:5]
        sec = 0
    ####################################################################
    time_temp = datetime.datetime(year, month, day, hour, min, sec)
    time_temp = str(time_temp.timestamp() * 1000)
    # 时间转化为时间戳ms毫秒
    #time_temp = str(time.mktime(time_temp.timetuple()) * 1000)
    #print(time_temp)

    # 合格/残次
    if id == "12_1" or id == "12_2" or id == "12_3" or id == "12_4":
        data = {
            "no": ID_TO_NO[id],
            "id": id,
            "name": MACHINE_ID_NAME[id],
            "value": ID_QUALIFIED_VALUE[id],
            "update_time": time_temp
        }

    elif id == "21" or id == "22":
        print(id)

    # 装配动作
    elif id == "21_1" or id == "21_2" or id == "21_3" or id == "21_4" or id == "21_5" or id == "21_6" \
            or id == "21_7" or id == "21_8" or id == "21_9" or id == "21_10" or id == "21_11" or id == "21_12":
        data = {
            "no": ID_TO_NO[id],
            "id": id,
            "name": "装配动作",
            "value": ACTION_ID_VALUE[id],
            "update_time": time_temp
        }

    # 装配结果
    elif id == "22_1" or id == "22_2" or id == "22_3" or id == "22_4" or id == "22_5" or id == "22_6" \
            or id == "22_7" or id == "22_8" or id == "22_9" or id == "22_10" or id == "22_11" or id == "22_12":
        data = {
            "no": ID_TO_NO[id],
            "id": id,
            "name": "装配结果",
            "value": RESULT_ID_VALUE[id],
            "update_time": time_temp
        }

    # 工位四电流、噪声、推力、震动
    elif id == "34" or id == "35" or id == "36" or id == "37":
        data = {
            "no": ID_TO_NO[id],
            "id": id,
            "name": MACHINE_ID_NAME[id],
            "value": pre_data["value"],
            "update_time": time_temp
        }

    else:
        data = {
            "no": ID_TO_NO[id],
            "id": id,
            "name": MACHINE_ID_NAME[id],
            "value": pre_data[id],
            "update_time": time_temp
        }
    return data


def img_data(data, tag):
    """
    图片格式化数据，预处理
    @param data:
    @param tag: 图片内容类型
    @return:
    """
    now_time = datetime.datetime.now()
    str_time = now_time.strftime('%y/%m/%d %H:%M:%S')
    str_time = time.strptime(str_time, '%y/%m/%d %H:%M:%S')
    year, month, day, hour, min, sec = str_time[:6]
    file_name = str(year) + '-' + str(month) + '-' + str(day) + '_' + str(hour) + '-' + str(min) + '-' + str(sec)
    img = {
        "tag": tag,
        "id": IMG_TAG_ID[tag],
        "name": IMG_TAG_NAME[tag],
        "value": str(file_name) + '_' + tag + '.jpg',  # 文件名value用'%Y-%m-%d_%H-%M-%S'字符串格式
        "data": data,
        "update_time": now_time
    }
    return img
