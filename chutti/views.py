from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render

# Create your views here.


def login(request):
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
                    "leave_request"
                )  # Redirect to the leave request page or any other page
            messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, "chutti/login.html", {"form": form})


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
