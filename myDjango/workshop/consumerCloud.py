# encoding=utf-8

# -----------------------------------------------------------------
# File Name:        consumerCloud.py
# Description:      边缘端与云端webSocket连接
# Date:             2021/4/13
# License:          (C)Copyright 2021, Bob
# Function List:
#
#
# -----------------------------------------------------------------


import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class CloudConsumer(WebsocketConsumer):
    room_name = ""
    room_group_name = ""

    def connect(self):
        self.room_name = 'cloud'  # self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))
