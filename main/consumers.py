import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# from django.contrib.auth.models import get_user_model
from .models import Room, Message, User
from channels.db import database_sync_to_async
from django.db.models import Prefetch
from datetime import datetime

# from django.contrib.auth import get_user_model


# User = get_user_model()
@database_sync_to_async
def get_room(user_room_messege):
    rooms = Room.objects.filter(members=user_room_messege)
    if rooms:
        # for room in rooms:
        #     print(room, "< --rooms")
        return rooms
        # return rooms, users_in_rooms
    return None


@database_sync_to_async
def get_room_mess(room_name):
    try:

        rooms = Room.objects.prefetch_related(
            Prefetch(
                "messages",
                queryset=Message.objects.all()[:6],
                # user=User.objects.get(username=request.user.username)
                to_attr="prefetched_messages",
            )
        ).all()

        print(rooms)

        # Пример обработки данных для вывода всех сообщений каждой комнаты
        dict_ = {}
        text = ""
        for room in rooms:
            print(f"Room: {room.name}")
            for message in room.prefetched_messages[1:]:
                print(f"Message: {message.text}, {message.user}, {message.created}")
                if room_name == room.name:
                    timestamp = str(message.created)
                    # Преобразование строки в объект datetime
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f%z")
                    # Форматирование объекта datetime в нужный формат строки
                    formatted_timestamp = dt.strftime("%Y-%m-%d %H:%M")
                    text += (
                        f"{message.text} от {message.user} - {formatted_timestamp}\n\n"
                    )
            dict_["room"] = text
        context = {"rooms": rooms}

    except Exception as e:
        print(e, "--- def main():")
    print(dict_)
    return dict_


class ChatConsumer(AsyncWebsocketConsumer):

    # =================================================
    async def connect(self):
        # self.room_name = "room"
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"
        query_string = self.scope["query_string"].decode()
        query_params = parse_qs(query_string)
        self.username = query_params.get("username", [None])[0]
        print(self.username)

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        print(f"{ self.room_group_name} - {self.username}: {message}")

        room, y = await Room.objects.aget_or_create(name=self.room_name)
        user, x = await User.objects.aget_or_create(username=self.username)
        await sync_to_async(user.rooms.add)(room)

        print(user, room)

        # создать сообщение и занести в поле messages модели Room
        message_obj = sync_to_async(room.add_message)(user, message)
        # print(await message_obj, "<<< -- message_obj")
        await message_obj

        # создать пользователя и занести в поле members модели Room
        user_obj_members = sync_to_async(room.add_user)(user)
        print(await user_obj_members, "< -------- user_obj_members")
        #
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        user_room_messege = await sync_to_async(
            User.objects.prefetch_related("rooms__messages").get
        )(username=self.username)
        # =================================================================
        print(f"User: {user_room_messege}")
        # print("members_set: ", user_room_messege.rooms.filter("members_set")
        print(f"room name: {self.room_name} ")
        print(f"id: {user_room_messege.id} ")

        dict_ = await get_room_mess(self.room_name)

        await self.send(text_data=json.dumps({"message": message, "dict": dict_}))
        #

        # =================================================================
        # message_obj = sync_to_async(Message.objects.filter)(user=user_room_messege)
        # print(message_obj)
        # rooms = await get_room(user_room_messege)
        # rooms_data = {}
        # rooms_list = []
        # for room in rooms:
        #     rooms_list.append(room)

        # rooms_data["name_room"] = room.name

        # print(rooms_data, "< --rooms")
        # print(users_in_rooms, "< -- users_in_rooms")
        # rooms_data = list(rooms.values())
        # =================================================================
        # text_data=json.dumps({"message": message, "rooms_data": rooms_data})
