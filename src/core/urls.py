from os import name
from django.urls import path

from .views import index, room, login, register, secret_route, logout

urlpatterns = [
    path("", index, name="index"),
    path("room/<int:room_id>", room, name="room"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("logout", logout, name="logout"),
    path("secret", secret_route, name="secret"),
]
