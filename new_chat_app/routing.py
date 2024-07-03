from django.urls import path, re_path
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter

from . import consumers

websocket_urlpatterns = [
    # path("ws/socket-server/", consumers.ChatConsumer.as_asgi()),
    path(
        "ws/v2/chat/<slug:room_id>/",
        consumers.ChatConsumer.as_asgi(),
        name="new_chat",
    ),
    path(
        "ws/v2/chat/<slug:room_id>/page/<slug:page_num>",
        consumers.ChatConsumer.as_asgi(),
        name="new_chat",
    ),
    # re_path(r"ws/socket-server/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
