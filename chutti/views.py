from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from chutti.services.util_services import login_required, logout_required

from .forms import LeaveForm
from .models import Leave

# Create your views here.


@logout_required
def login(request: HttpRequest):
    error_message = ""
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                django_login(request, user)
                return redirect("dashboard")
            error_message = "Invalid username or password."
        else:
            error_message = "Invalid username or password."
    return render(request, "chutti/login.html", {"error_message": error_message})


@logout_required
def signup(request: HttpRequest):
    error_message = ""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to the login page

        error_message = next(iter(next(iter(form.errors.values()))))
    else:
        form = UserCreationForm()
    return render(request, "chutti/signup.html", {"error_message": error_message})


@require_http_methods(["GET"])
def logout(request: HttpRequest):
    django_logout(request)
    return redirect("login")


@require_http_methods(["GET"])
@login_required
def dashboard(request: HttpRequest):
    leaves_applied = Leave.objects.filter(user=request.user).order_by("-date_of_leave")
    leave_counts = {}
    for leave in leaves_applied:
        if leave.leave_type not in leave_counts:
            leave_counts[leave.leave_type] = 0

        leave_counts[leave.leave_type] += 1

    return render(
        request,
        "chutti/dashboard.html",
        {"leaves_applied": leaves_applied, "leave_counts": leave_counts},
    )


@login_required
def apply(request: HttpRequest):
    error_message = ""
    if request.method == "POST":
        form = LeaveForm(request.POST)
        if form.is_valid():
            error_message = form.save(user=request.user)
            if not error_message:
                return redirect("dashboard")
        else:
            error_message = next(iter(next(iter(form.errors.values()))))
    else:
        form = LeaveForm()
    return render(
        request, "chutti/apply.html", {"form": form, "error_message": error_message}
    )
