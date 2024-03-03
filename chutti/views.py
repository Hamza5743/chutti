from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .models import Leave, LeaveHours

# Create your views here.


def login(request):
    error_message = ""
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                messages.success(request, f"Welcome, {username}!")
                return redirect(
                    "signup"
                )  # Redirect to the leave request page or any other page
            error_message = "Invalid username or password."
        else:
            error_message = "Invalid username or password."
    return render(request, "chutti/login.html", {"error_message": error_message})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}. You can now log in."
            )
            return redirect("login")  # Redirect to the login page
    else:
        form = UserCreationForm()
    return render(request, "chutti/signup.html", {"form": form})


def get_leaves(request):
    leaves: list[Leave] = Leave.objects.filter()
    for l in leaves:
        print(l.date_of_leave)
        print(l.leave_hours)
        print(l.user)
    return HttpResponse("Success")


def make_data(request: HttpRequest):
    from datetime import datetime

    if request.user.is_authenticated:
        for j in range(4):
            l = Leave(user=request.user, date_of_leave=datetime.now().date())
            if j % 2 == 0:
                l.leave_hours = LeaveHours.PARTIAL_LEAVE
            l.save()

        return HttpResponse("Success")

    return HttpResponse("Failure")
