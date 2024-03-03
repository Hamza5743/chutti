from django.urls import path

from .views import dashboard, get_leaves, login, logout, make_data, signup

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("create/", make_data, name="make_data"),
    path("getall/", get_leaves, name="get_leaves"),
]
