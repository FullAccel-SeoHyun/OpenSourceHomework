# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        User.objects.create_user(username=username, password=password)
        return redirect("login")

    return render(request, "accounts/signup.html")


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("my_tickets")   # 로그인 후 이동

        return render(request, "accounts/login.html", {"error": "로그인 실패!"})

    return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return redirect("login")