# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
import re


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % re.sub(r'\W+', '', self.room_name)
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        #add user
        self.user = self.scope["user"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'userlist_update',
                'add_user': str(self.user)
            }
        )
        await self.accept()


    async def disconnect(self, close_code):
        

        #delete user
        self.user = self.scope["user"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'userlist_update',
                'delete_user': str(self.user)
            }
        )
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def userlist_update(self, event):

        if 'add_user' in event:
            add_user = event['add_user']
            #send message to Websocket
            await self.send(text_data=json.dumps({
                'add_user':add_user
            }))
        if 'delete_user' in event:
            delete_user = event['delete_user']
            #send message to Websocket
            await self.send(text_data=json.dumps({
                'delete_user':delete_user
            }))


    # Receive message from WebSocket, only for text message
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['chattext']
        sender = text_data_json['sender']
        timestamp = text_data_json['timestamp']
        isText = text_data_json['isText']
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender' : sender,
                'timestamp': timestamp,
                'isText': isText,
            }
        )

    # Receive message from room group, only for text message
    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']
        isText = event['isText']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender' : sender,
            'timestamp': timestamp,
            'isText':isText,
        }))
