from django.shortcuts import redirect, render
from .models import Message, Room, User


# def index(request, *args, **kwargs):

#     mes = Message.objects.all().order_by("-created")[:5]

#     return render(request, "main.html", {"mes": mes})

from django.shortcuts import render
from django.db.models import Prefetch


# def index(request):
#     try:

#         rooms = Room.objects.prefetch_related(
#             Prefetch(
#                 "messages",
#                 queryset=Message.objects.all()[:5],
#                 # user=User.objects.get(username=request.user.username)
#                 to_attr="prefetched_messages",
#             )
#         ).all()

#         # Пример обработки данных для вывода всех сообщений каждой комнаты
#         for room in rooms:
#             print(f"Room: {room.name}")
#             for message in room.prefetched_messages:
#                 print(f"Message: {message.text}, {message.user}, {message.created}")
#         context = {"rooms": rooms}
#     except Exception as e:
#         print(e, "--- def main():")
#     return render(request, "room.html", context)


def main(request, *args, **kwargs):
    """Получить все комнаты и связанные сообщения (5шт) пользователя"""
    # print(request.user.username)
    try:

        rooms = Room.objects.prefetch_related(
            Prefetch(
                "messages",
                queryset=Message.objects.all()[:5],
                # user=User.objects.get(username=request.user.username)
                to_attr="prefetched_messages",
            )
        ).all()

        # Пример обработки данных для вывода всех сообщений каждой комнаты
        for room in rooms:
            print(f"Room: {room.name}")
            for message in room.prefetched_messages:
                print(f"Message: {message.text}, {message.user}, {message.created}")
        context = {"rooms": rooms}
    except Exception as e:
        print(e, "--- def main():")
    x = render(request, "main.html", context)
    # return render(request, "menu.html", context)
    return x


def room(request, room_id, num=None):
    print(room_id, "< --- room id: ")
    print(num, "< --- num page: ")
    # mes = Message.objects.all().order_by("-created")[:5]
    from django.shortcuts import get_object_or_404

    room = Room.objects.get(id=room_id)
    print(room)
    return render(request, "new_room.html", {"room": room, "num": num})


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
