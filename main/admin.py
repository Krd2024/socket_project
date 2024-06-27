from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Room, Message, User

CustomUser = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


admin.site.register(Room)
admin.site.register(Message)

# Register your models here.
