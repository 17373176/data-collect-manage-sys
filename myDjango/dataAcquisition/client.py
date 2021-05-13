# encoding=utf-8
# !/usr/bin/env python

# -----------------------------------------------------------------
# File Name:        client.py
# Description:      数据采集客户端
# Date:             2021/3/9
# License:          (C)Copyright 2021, Bob
# Function List:    创建客户端，建立安全通道，创建会话
#                   用户验证，加载证书和私钥进行验证
#                   连接服务器端口
#                   数据订阅
#
# -----------------------------------------------------------------


import time
import opcua
import opcua.crypto.uacrypto


def data_acquisition(request):
    """
    OPC UA数据采集
    @return:
    """
    # OPC UA客户端连接到服务器，通过TCP连接，更换host和端口号
    opcua_client = opcua.Client("opc.tcp://localhost:4840/opcua/server/")
    try:
        client.set_user("opcua")  # 设置用户名和密码
        client.set_password("123456")
        client.set_security_string("Basic256Sha256,"
                                   "SignAndEncrypt,"
                                   "../../myDjango/cert/client_cert.pem,"
                                   "../../myDjango/cert/client_key.pem,"
                                   "../../myDjango/cert/server_cert.pem")  # 添加认证证书和密钥

        opcua_client.connect()  # 建立连接，无返回值，连接失败会直接抛出异常
        # if conn is None:  # 连接失败
        #    msgResponse.ExceptionHandle(conn, 'data_server_con_failed')
        # 获得节点
        root = opcua_client.get_root_node()
        print("Objects node is: ", root)
        print("Children of root are: ", root.get_children())  # 读取节点属性

        # 通过路径获得节点变量
        while True:
            my_var = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
            obj = root.get_child(["0:Objects", "2:MyObject"])
            print("myVar is: ", my_var)
            print("myObj is: ", obj)

            # Stacked myvar access
            print("myVar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())
            time.sleep(2)
    finally:
        opcua_client.disconnect()

