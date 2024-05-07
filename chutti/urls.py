from django.urls import path

from .views import add_leaves, apply, dashboard, login, logout, signup

urlpatterns = [
    path("", login, name="root"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/<int:pk>/", dashboard, name="dashboard"),
    path("apply/", apply, name="apply"),
    path("add/leaves/", add_leaves, name="add_leaves"),
]
