from django.urls import path

from core.views.room import index, room, enter_flag, unlock_conclusion, user_content_tracker
from core.views.auth import login, logout, register
from core.views.user import profile, scoreboard
from core.views.sqli_test import get_sql_response

urlpatterns = [
    path("", index, name="index"),
    path("room/<int:pk>/", room, name="room"),
    path("room/<int:room_id>/enter-flag/", enter_flag, name="enter_flag"),
    path("room/<int:room_id>/unlock/", unlock_conclusion, name="unlock_conclusion"),
    path("room/<int:room_id>/track", user_content_tracker, name="user_content_tracker"),
    path("login/", login, name="login"),
    path("register/", register, name="register"),
    path("logout/", logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("scoreboard/", scoreboard, name="scoreboard"),
    path("sqli-execute/", get_sql_response, name="sqli-execute"),
]
