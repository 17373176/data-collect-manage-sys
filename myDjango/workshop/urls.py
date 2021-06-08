# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        workshop\urls.py
# Description:      配置相应函数路径映射
# Function List:    将views.py文件里的函数操作添加进来
# -----------------------------------------------------------------


from django.urls import path
from workshop import views, dataBaseDao, consumerUI
from dataAcquisition import multiProtocol

# 可以利用正则表达式匹配url,也可以使用二级路由
urlpatterns = [
    path('', views.index, name='index'),
    path('room', views.room),

    path('WorkshopConsumer', consumerUI.WorkshopConsumer),

    path('test', views.test),

    path('websocket_send_to_user', views.websocket_send_to_user),
    path('add_static_info', views.add_static_info),

    # 前端访问数据库
    path('data/sendAll', views.data_send_all),  # webSocket主动传送给前端
    path('data/getRobotInfoOne', views.query_workshop1),
    path('data/getRobotInfoTwo', views.query_workshop2),
    path('data/getAll', views.data_get_all),


    # 接收工位1的数据
    path('data/set1', multiProtocol.insert_data_set),
    # 接收工位2的数据
    path('data/set2', multiProtocol.insert_data_set),
    # 接收工位3-1的数据
    path('data/set3', multiProtocol.insert_data_set),
    # 接收工位3-2的数据
    path('data/set4', multiProtocol.insert_data_set),
    # 接收工位4的数据
    path('data/set5', multiProtocol.insert_data_set),

    # 接收工位1上图片1
    path('file/binary/upload/loading1', multiProtocol.file_upload_L1),
    # 接收工位1上图片2
    path('file/binary/upload/loading2', multiProtocol.file_upload_L2),
    # 接收工位2上图片
    path('file/binary/upload/reg', multiProtocol.file_upload_reg),
    # 接收工位3上动作图片
    path('file/binary/upload/action', multiProtocol.file_upload_action),
    # 接收工位3上检测图片
    path('file/binary/upload/result', multiProtocol.file_upload_result),

]

'''
    # 接收工位1上图片1
    path('file/binary/upload/loading1', multiProtocol.file_upload_L1),
    # 接收工位1上图片2
    path('file/binary/upload/loading2', multiProtocol.file_upload_L2),
    # 接收工位2上图片
    path('file/binary/upload/reg', multiProtocol.file_upload_reg),
    # 接收工位3上动作图片
    path('file/binary/upload/action', multiProtocol.file_upload_action),
    # 接收工位3上检测图片
    path('file/binary/upload/result', multiProtocol.file_upload_result),
    '''
