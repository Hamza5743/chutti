from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.db import transaction
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from chutti import forms
from chutti.models import Leave, LeavesLeft, LeaveType, UserConstants
from chutti.services.util_services import login_required, logout_required


@logout_required
def login(request: HttpRequest):
    error_message = ""
    if request.method == "POST":
        form = forms.LoginForm(request, request.POST)
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
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Redirect to the login page

        error_message = next(iter(next(iter(form.errors.values()))))
    else:
        form = forms.SignUpForm()
    return render(request, "chutti/signup.html", {"error_message": error_message})


@require_http_methods(["GET"])
def logout(request: HttpRequest):
    django_logout(request)
    return redirect("login")


@require_http_methods(["GET", "POST"])
@login_required
def dashboard(request: HttpRequest, pk=None):
    if request.method == "POST":
        with transaction.atomic():
            leave_to_delete: Leave = Leave.objects.get(pk=pk)
            if leave_to_delete:
                leaves_left = LeavesLeft.get_current_object(user=request.user)
                leave_type_left = getattr(
                    leaves_left,
                    leaves_left.convert_leave_name_to_attribute(
                        leave_to_delete.leave_type
                    ),
                )

                setattr(
                    leaves_left,
                    leaves_left.convert_leave_name_to_attribute(
                        leave_to_delete.leave_type
                    ),
                    leave_type_left + 1,
                )

                leaves_left.save()
                leave_to_delete.delete()

    leaves_applied = Leave.objects.filter(user=request.user).order_by("-date_of_leave")
    leaves_left = LeavesLeft.get_current_object(user=request.user)
    leave_counts = {}
    for leave in leaves_applied:
        if leave.leave_type not in leave_counts:
            leave_counts[leave.leave_type] = {
                "leaves_taken": 0,
                "leaves_left": getattr(
                    leaves_left,
                    leaves_left.convert_leave_name_to_attribute(leave.leave_type),
                    0,
                ),
            }

        leave_counts[leave.leave_type]["leaves_taken"] += 1
        leave_counts[leave.leave_type]["leaves_left"] += 1

    for leave_type in LeaveType.choices:
        if leave_type[1] not in leave_counts:
            leave_counts[leave_type[1]] = {
                "leaves_taken": 0,
                "leaves_left": getattr(
                    leaves_left,
                    leaves_left.convert_leave_name_to_attribute(leave_type[1]),
                    0,
                ),
            }

    return render(
        request,
        "chutti/dashboard.html",
        {"leaves_applied": leaves_applied, "leave_counts": leave_counts},
    )


@login_required
def apply(request: HttpRequest):
    error_message = ""
    if request.method == "POST":
        form = forms.LeaveForm(request.POST)
        if form.is_valid():
            error_message = form.save(user=request.user)
            if not error_message:
                return redirect("dashboard")
        else:
            error_message = next(iter(next(iter(form.errors.values()))))
    else:
        form = forms.LeaveForm()
    return render(
        request, "chutti/apply.html", {"form": form, "error_message": error_message}
    )


@login_required
def add_leaves(request: HttpRequest):
    user_constants = next(
        iter(UserConstants.objects.filter(user=request.user)),
        None,
    )

    if user_constants and user_constants.has_seen_add_leaves_page:
        return redirect("/")

    error_message = ""
    if request.method == "POST":
        form = forms.AddLeavesForm(request.POST)
        if form.is_valid():
            error_message = form.save(user=request.user)
            if not error_message:
                return redirect("dashboard")
        else:
            error_message = next(iter(next(iter(form.errors.values()))))
    else:
        form = forms.AddLeavesForm()
    return render(
        request, "chutti/addLeaves.html", {"form": form, "error_message": error_message}
    )
