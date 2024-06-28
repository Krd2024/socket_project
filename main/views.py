from django.shortcuts import redirect, render
from .models import Message, User


# def index(request, *args, **kwargs):

#     mes = Message.objects.all().order_by("-created")[:5]

#     return render(request, "main.html", {"mes": mes})

from django.shortcuts import render


def index(request):
    return render(request, "room.html")


def main(request, *args, **kwargs):

    return render(request, "main.html")


def room(request, room_name):
    print(room_name)
    # mes = Message.objects.all().order_by("-created")[:5]
    return render(request, "room.html", {"room_name": room_name})


def user_profile(request):
    try:
        user = request.user
        objects_user = User.objects.get(username=user)
    except Exception as e:
        print(e, "<< ------ def user_profile():")
        return redirect("index")

    # if request.GET.get("q") == "questions":
    #     user_question = Question.objects.filter(autor=objects_user)
    #     context = {
    #         "user_question": user_question,
    #     }

    # return render(request, "user_profile.html", {"username": objects_user})
