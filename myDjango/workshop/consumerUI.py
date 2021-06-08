# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        consumerUI.py
# Description:      和前端建立webSocket通信的类
# Date:             2021/4/19
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------


import json
from channels.generic.websocket import AsyncWebsocketConsumer


class WorkshopConsumer(AsyncWebsocketConsumer):
    workshop_name = ''
    workshop_group_name = ''

    async def connect(self):
        # connection information is in self.scope
        self.workshop_name = self.scope['url_route']['kwargs']['workshop_name']
        # group name
        self.workshop_group_name = 'group_%s' % self.workshop_name

        # add to a group, use async_to_sync wrapper
        await self.channel_layer.group_add(
            self.workshop_group_name,
            self.channel_name
        )
        # accept connection (if want to implement access deny, do it here)
        await self.accept()

    async def disconnect(self, close_code):
        # leave a group
        await self.channel_layer.group_discard(
            self.workshop_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # 发送一个消息到组
        # 组中的接受者在接收后调用chat_message()方法
        await self.channel_layer.group_send(
            self.workshop_group_name,
            {
                'type': 'workshop_message',
                'message': message
            }
        )

    # Handling Function: convert data to websocket message
    async def workshop_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
