#  encoding=utf-8
# !/usr/bin/env python

# -----------------------------------------------------------------
# File Name:        opcuaClient.py
# Description:      OPU UA客户端
# Function List:    客户端连接服务器 -- client = Client()
#                   访问头结点 -- idx
#                   读取节点属性 -- objects
#
#
#
# -----------------------------------------------------------------

import sys
import time
from opcua import ua, Client
from Server import opcuaServer
sys.path.insert(0, "..")


if __name__ == "__main__":
    opcuaServer.opcua_server()

    # 客户端连接到服务器，通过TCP连接，host为服务器那边的地址
    client = Client("opc.tcp://localhost:4840/opcua/server/")
    client.set_user("opcua")  # 设置用户名和密码
    client.set_password("123456")
    client.set_security_string("Basic256Sha256,"
                               "SignAndEncrypt," 
                               "../../myDjango/cert/client_cert.pem,"
                               "../../myDjango/cert/client_key.pem,"
                               "../../myDjango/cert/server_cert.pem")  # 验证证书密钥

    try:
        client.connect()
        # 获得节点Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)
        print("Children of root are: ", root.get_children())  # 读取节点属性，node attributes as well as browse or populate address space

        # 查看节点属性值
        # var = client.get_node(ua.NodeId(1002, 2))
        # var = client.get_node("ns=3;i=2002")
        # print(var)
        # var.get_data_value() # get value of node as a DataValue object
        # var.get_value() # get value of node as a python builtin
        # var.set_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        # var.set_value(3.9) # set node value using implicit data type

        # 通过路径获得节点变量
        '''
        while True:
            myVar = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
            obj = root.get_child(["0:Objects", "2:MyObject"])
            print("myVar is: ", myVar)
            print("myObj is: ", obj)

            # Stacked myvar access
            print("myVar is: ", root.get_children()[0].get_children()[1].get_variables()[0].get_value())
            time.sleep(2)
        '''
    finally:
        client.disconnect()
