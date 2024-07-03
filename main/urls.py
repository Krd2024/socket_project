from django import views
from .views import main, room, user_profile
from django.contrib import admin
from django.urls import include, path
from main import auth


urlpatterns = [
    path("", main, name="main"),
    path("room/<int:room_id>/", room, name="room"),
    path("room/<int:room_id>/page/<int:num>", room, name="room_page"),
    # path("", index, name="index"),
    #
    path("signup/", auth.signup, name="signup"),
    path("login_in/", auth.login_in, name="login_in"),
    path("login/", auth.CustomLoginView.as_view(), name="login"),
    path("logout/", auth.logoutPage, name="logout"),
    #
    path("user/<str:username>/", user_profile, name="user_profile"),
]
