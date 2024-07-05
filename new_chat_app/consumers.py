import json
import math
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

# from django.contrib.auth.models import get_user_model
from main.models import Room, Message, User
from channels.db import database_sync_to_async
from django.db.models import Prefetch
from datetime import datetime
from django.template.loader import render_to_string

LIMIT_OF_USERS_ON_PAGE = 5


class ChatConsumer(WebsocketConsumer):
    def connect(self, **kwargs):
        self.accept()
        room_id = self.scope["url_route"]["kwargs"]["room_id"]
        page = self.scope["url_route"]["kwargs"]["page_num"]
        query_string = self.scope["query_string"].decode()

        self.room_group_name = f"chat_{room_id}"
        #
        self.channel_layer.group_add(self.room_group_name, self.channel_name)
        query_params = parse_qs(query_string)

        self.user_id = query_params.get("user_id", [None])[0]
        # room_id = kwargs.get('roomid')
        room_obj = Room.objects.get(id=room_id)
        messages = room_obj.messages.all()
        # =================================================================
        print(page, "< --- page")
        try:
            if page is not None:
                try:
                    page = int(page)
                    if page < 2:
                        raise ValueError()
                except:
                    ...
                    # return redirect("all_users")
            else:
                page = 1

            num_pages = int(math.ceil(len(messages) / LIMIT_OF_USERS_ON_PAGE))
            users_per_page = LIMIT_OF_USERS_ON_PAGE
            paginator = Paginator(messages, users_per_page)  # Создаем пагинатор
        except Exception as e:
            print(e)

        if num_pages <= 15:
            start = 1
            end = num_pages + 1
        else:
            start = max(1, page - 5)
            end = min(page + 5, num_pages + 1)

            # Корректировка диапазона, если он выходит за пределы допустимых значений
            if end - start < 10:
                if start == 1:
                    end = 11
                elif end == num_pages + 1:
                    end = num_pages - 9
        if page > 5:
            page_range = range(page - 5, min(page + 5, paginator.num_pages + 1))
        else:
            page_range = range(1, min(page + 10, paginator.num_pages + 1))

        try:
            sorted_users = paginator.page(page)
        except PageNotAnInteger:
            sorted_users = paginator.page(1)
        except EmptyPage:
            sorted_users = paginator.page(paginator.num_pages)

        context = {
            "room_id": room_id,
            "page_number": page,
            "pages_range": page_range,
            "messages": sorted_users,
        }

        html_string = render_to_string("new_chat_app/messages.html", context)
        self.send(text_data=html_string)

    def disconnect(self, code):
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    def receive(self, text_data=None, bytes_data=None):

        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        room_id = self.scope["url_route"]["kwargs"]["room_id"]

        room, x = Room.objects.get_or_create(id=room_id)
        user, y = User.objects.get_or_create(id=self.user_id)
        print(user, room)

        add = user.rooms.add(room)
        print(add)
        room.add_message(user, message)
        room.add_user(user)

        x = self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message},
        )
        self.send(text_data=json.dumps({"message": message}))
        # print(x)

    # def chat_message(self, event=None):
    #     print(event, "<------- event")
    #     message = event["message"]
    #     print(message, "<------ message")

    # context = {"message": message}
    # html_string = render_to_string("new_chat_app/messages.html", context)
    # self.send(text_data=html_string)
    # self.send(text_data=json.dumps({"message": message}))
    #

    # async def chat_message(self, event=None):
    #     message = event["message"]

    #     print(f"room name: {self.room_name} ")
    #     await self.send(text_data=json.dumps({"message": message}))
    #     #
