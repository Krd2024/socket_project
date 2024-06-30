from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView

from django.shortcuts import render, redirect

from .forms import UserRegisterForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from main.models import User


def logoutPage(request):
    logout(request)
    return redirect("main")


def login_in(request):
    return render(request, "login_in.html")


def signup(request):
    if request.method == "POST":

        form = UserRegisterForm(request.POST)
        # form = ProfileEditForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("login_in")
    else:
        form = UserRegisterForm()
    return render(request, "signup.html", {"form": form})


class CustomLoginView(LoginView):

    def post(self, request):
        print(request.GET, "<<<<<<< ========")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Проверка аутентификации пользователя
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            # return redirect(
            #     f"/user/{username}"
            #     # f"/user/"
            # )
            return redirect("main")
        else:
            return render(
                request,
                "login_in.html",
                {"error_message": "Неправильный логин или пароль"},
            )
