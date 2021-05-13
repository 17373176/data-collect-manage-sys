# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        routing.py
# Description:      与前端webSocket通信路由配置
# Date:             2021/4/19
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------


from django.urls import re_path

from . import consumerUI

websocket_urlpatterns = [
    re_path(r'ws/workshop/room/', consumerUI.WorkshopConsumer.as_asgi()),
]