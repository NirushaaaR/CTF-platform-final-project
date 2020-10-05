from django.urls import path

from core.views.room import index, room, enter_flag
from core.views.auth import login, logout, register
from core.views.user import profile, scoreboard

urlpatterns = [
    path("", index, name="index"),
    path("room/<int:pk>", room, name="room"),
    path("room/<int:room_id>/enter-flag", enter_flag, name="enter_flag"),
    path("login", login, name="login"),
    path("register", register, name="register"),
    path("logout", logout, name="logout"),
    path("profile", profile, name="profile"),
    path("scoreboard", scoreboard, name="scoreboard"),
]
