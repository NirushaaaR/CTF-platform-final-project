from os import name
from django.urls import path

from .views import (
    index,
    room,
    login,
    register,
    secret_route,
    logout,
    enter_flag,
)

urlpatterns = [
    path("", index, name="index"),
    path("room/<int:pk>", room, name="room"),
    path("room/<int:room_id>/enter-flag", enter_flag, name="enter_flag"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("logout", logout, name="logout"),
    path("secret", secret_route, name="secret"),
]
