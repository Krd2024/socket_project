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
# @sync_to_async
def get_user(username):
    return User.objects.get(username=username)


@sync_to_async
def get_user_messages(user):
    return Message.objects.filter(user=user)


async def get_messages(user):
    user_obj = await get_user(user)
    messages = await get_user_messages(user_obj)
    return messages


class ChatConsumer(AsyncWebsocketConsumer):

    # async def get_all_messages(self):
    #     x = await sync_to_async( Message.objects.all)()
    #     return x

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        query_string = self.scope["query_string"].decode()
        query_params = parse_qs(query_string)
        self.username = query_params.get("username", [None])[0]
        print(self.username)

        print("hello")
        await self.accept()
        res = await get_messages(self.username)
        print(res)
        # m =  await get_messages(self.username)
        # print(m)
        # # x = render_to_string("new_chat_app/messages.html", {"messages": m})

        # await self.send(text_data=x)

    async def disconnect(self, code):
        ...

    async def receive(self, text_data=None, bytes_data=None):

        ...
