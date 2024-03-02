from django.urls import path

from .views import get_leaves, login, make_data, signup

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("create/", make_data, name="make_data"),
    path("getall/", get_leaves, name="get_leaves"),
]
