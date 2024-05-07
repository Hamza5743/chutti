from functools import wraps

from django.http import HttpRequest
from django.shortcuts import redirect

from chutti.models import UserConstants


def logout_required(view):

    @wraps(view)
    def check_logout(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            # User has an active session
            return redirect("dashboard")

        return view(request, *args, **kwargs)

    return check_logout


def login_required(view):

    @wraps(view)
    def check_login(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            # User has an active session
            return redirect("login")

        user_constants = next(
            iter(UserConstants.objects.filter(user=request.user)),
            None,
        )

        if (
            not (user_constants and user_constants.has_seen_add_leaves_page)
            and request.path != "/add/leaves/"
        ):
            return redirect("add_leaves")

        return view(request, *args, **kwargs)

    return check_login
