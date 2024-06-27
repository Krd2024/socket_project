from django.urls import path

from . import consumers, views

websocket_urlpatterns = [
    path("ws/socket-server", consumers.ChatConsumer.as_asgi()),
    path(
        "ws/socket-server/<str:room_name>/",
        consumers.ChatConsumer.as_asgi(),
        name="room",
    ),
]
