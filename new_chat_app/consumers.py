import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.shortcuts import render

# from django.contrib.auth.models import get_user_model
from main.models import Room, Message, User
from channels.db import database_sync_to_async
from django.db.models import Prefetch
from datetime import datetime
from django.template.loader import render_to_string


@database_sync_to_async
def get_messages():
    return Message.objects.all()


class ChatConsumer(AsyncWebsocketConsumer):
    
    
    async def get_all_messages(self):
        x = await sync_to_async( Message.objects.all)()
        return x

    async def connect(self):

        print("hello")

        await self.accept()
        m =  await self.get_all_messages()
        print(m)
        x = render_to_string("new_chat_app/messages.html", {"messages": m})

        await self.send(text_data=x)

    async def disconnect(self, code):
        ...

    async def receive(self, text_data=None, bytes_data=None):

        ...
