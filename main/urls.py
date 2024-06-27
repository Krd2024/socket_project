from .views import index, room
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("", index, name="index"),
    path("<str:room_name>/", room, name="room"),
]
