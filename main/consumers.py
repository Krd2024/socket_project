import json
from urllib.parse import parse_qs

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# from django.contrib.auth.models import get_user_model
from .models import Room, Message, User

# User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
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
        # username = text_data_json["username"]
        print(f"{ self.room_group_name} - {self.username}: {message}")

        # user = sync_to_async(User.objects.aget_or_create)(username=self.username)
        user, x = await User.objects.aget_or_create(username=self.username)

        # room = sync_to_async(Room.objects.aget_or_create)(name=self.room_name)
        room, y = await Room.objects.aget_or_create(name=self.room_name)

        # message_instance = sync_to_async(Message.objects.create)(
        #     user=user, text=message
        # )
        message_instance, z = await Message.objects.aget_or_create(
            user=user, text=message
        )

        # z = await message_instance

        print(user, room)
        sync_to_async(room.add_message)(user, message_instance)
        #
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message},
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message}))
