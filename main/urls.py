from django import views
from .views import main, room, index
from django.contrib import admin
from django.urls import include, path
from main import auth


urlpatterns = [
    # path("", main, name="main"),
    path("<str:room_name>/", room, name="room"),
    path("", index, name="index"),
    #
    path("signup/", auth.signup, name="signup"),
    path("login/", auth.CustomLoginView.as_view(), name="login"),
]
