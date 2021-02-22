from django.urls import path

from core.views.room import index, room, enter_flag, room_by_tag
from core.views.auth import login, logout, register, validate_email, validate_username
from core.views.user import profile, scoreboard

urlpatterns = [
    path("", index, name="index"),
    path("tag/<str:tag>", room_by_tag, name="room_by_tag"),
    path("room/<int:pk>/", room, name="room"),
    path("room/<int:room_id>/enter-flag/", enter_flag, name="enter_flag"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("validate_username/", validate_username, name="validate_username"),
    path("validate_email/", validate_email, name="validate_email"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("scoreboard/", scoreboard, name="scoreboard"),
]
