from os import name
from django.urls import path

from .views import index, room, login, register

urlpatterns = [
    path("", index, name="index"),
    path("room/<int:room_id>", room, name="room"),
    path("login", login, name="login"),
    path("register", register, name="register"),
]
