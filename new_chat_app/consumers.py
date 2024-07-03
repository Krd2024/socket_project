import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from django.shortcuts import render

# from django.contrib.auth.models import get_user_model
from main.models import Room, Message, User
from channels.db import database_sync_to_async
from django.db.models import Prefetch
from datetime import datetime
from django.template.loader import render_to_string


class ChatConsumer(WebsocketConsumer):
    def connect(self,  **kwargs):
        self.accept()
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        # room_id = kwargs.get('roomid')
        room_obj = Room.objects.get(id=room_id)

        messages = room_obj.messages.all()
       

        html_string = render_to_string("new_chat_app/messages.html", {"messages": messages})
        self.send(text_data=html_string)

    def disconnect(self, code):
        ...

    def receive(self, text_data=None, bytes_data=None):

        ...
