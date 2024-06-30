from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    rooms = models.ManyToManyField("Room", related_name="members_set", blank=True)


from django.db import models
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async

# User = get_user_model()


class Room(models.Model):
    name = models.CharField(max_length=255)
    messages = models.ManyToManyField("Message", related_name="rooms_set", blank=True)
    members = models.ManyToManyField(User, related_name="users_set", blank=True)

    def __str__(self):
        return self.name

    @property
    def get_messages(self, room=None):
        message = self.Room.object.filter(messages=164)
        return message

    # @sync_to_async

    def add_user(self, user):
        self.members.add(user)

    # @sync_to_async
    def remove_user(self, user):
        self.members.remove(user)

    # @sync_to_async
    def add_message(self, user, text):
        message = Message.objects.create(user=user, text=text)
        self.messages.add(message)
        return message


class Message(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, related_name="messages", on_delete=models.SET_NULL
    )
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]} ({self.created})"
