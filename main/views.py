from django.shortcuts import render
from .models import Message


# def index(request, *args, **kwargs):

#     mes = Message.objects.all().order_by("-created")[:5]

#     return render(request, "main.html", {"mes": mes})

from django.shortcuts import render


def index(request):
    return render(request, "room.html")


# def room(request, room_name):
#     return render(request, "chat/room.html", {"room_name": room_name})


def main(request, *args, **kwargs):

    return render(request, "main.html")


def room(request, room_name):
    print(room_name)
    # mes = Message.objects.all().order_by("-created")[:5]
    return render(request, "room.html", {"room_name": room_name})
