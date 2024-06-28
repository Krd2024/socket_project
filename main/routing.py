from django.urls import path, re_path
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from . import consumers
from . import consumers, views

websocket_urlpatterns = [
    # path("ws/socket-server/", consumers.ChatConsumer.as_asgi()),
    path(
        "ws/socket-server/<str:room_name>/",
        consumers.ChatConsumer.as_asgi(),
        name="main_chat",
    ),
    # re_path(r"ws/socket-server/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
# application = ProtocolTypeRouter(
#     {
#         "websocket": URLRouter(websocket_urlpatterns),
#     }
# )
