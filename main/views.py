from django.shortcuts import render
from .models import Message


def index(request, *args, **kwargs):

    mes = Message.objects.all().order_by("-created")[:5]

    return render(request, "index.html", {"mes": mes})


def room(request, room_name):
    print(room_name)
    # mes = Message.objects.all().order_by("-created")[:5]
    return render(request, "room.html", {"room_name": room_name})
