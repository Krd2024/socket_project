from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):
    rooms = models.ManyToManyField("Room", related_name="users", blank=True)

    # user_permissions = models.ManyToManyField(
    #     Permission,
    #     related_name="customuser_set",
    #     blank=True,
    #     help_text="Specific permissions for this user.",
    #     verbose_name="user permissions",
    # )


class Room(models.Model):
    name = models.CharField(max_length=255)
    # Можно добавить дополнительные поля для модели Room, если необходимо

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, related_name="messages", on_delete=models.SET_NULL
    )
    text = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    rooms = models.ManyToManyField(Room, related_name="messages")

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]} ({self.created})"
