from django.urls import path

from .views import apply, dashboard, login, logout, signup

urlpatterns = [
    path("", login, name="root"),
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("dashboard/<int:pk>/", dashboard, name="dashboard"),
    path("apply/", apply, name="apply"),
]
