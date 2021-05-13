#  encoding=utf-8
# !/usr/bin/env python

# -----------------------------------------------------------------
# File Name:        opcuaServer.py
# Description:      OPU UA服务器
# Function List:    创建服务器对象 -- server = Server()
#                   建立地址空间 -- idx
#                   获取对象节点 -- objects
#                   完成节点与地址空间的映射
#                   开启服务器 -- start()
#
# -----------------------------------------------------------------

import sys
import time
from opcua import ua, Server, crypto
sys.path.insert(0, "..")


def opcua_server():

    dataLib = ("") #

    # 创建服务器对象，配置服务器url
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/opcua/server/")

    # 建立地址空间
    url = "http://examples.opcua.github.io"
    idx = server.register_namespace(url)  # 注册地址空间

    # server.import_xml('../node.xml')  # 导入自定义xml数据

    # 获得对象节点get Objects node, this is where we should put our nodes
    #objects = server.get_objects_node()

    # 添加节点，映射地址空间
    #myObj = objects.add_object(idx, "MyObject")  # 添加对象节点
    #myVar = myObj.add_variable(idx, "MyVariable", 6.7)  # 添加变量节点
    #myVar.set_writable()  # 写入Set MyVariable as writable by clients

    # 开启服务器
    server.set_security_policy([
                            ua.SecurityPolicyType.NoSecurity,
                            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
                            ua.SecurityPolicyType.Basic256Sha256_Sign
                                ])  # 选定支持的安全策略
    server.load_certificate("../../myDjango/cert/server_cert.pem")
    server.load_private_key("../../myDjango/cert/server_key.pem")
    server.start()


'''
    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            myVar.set_value(count)  # 对节点设置值Set value of a node
    finally:
        # 关闭服务器连接，取消订阅
        server.stop()

'''
