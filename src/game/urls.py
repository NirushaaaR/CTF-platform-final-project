# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="game_index"),
    path("<str:game_slug>/", views.game_view, name="game"),
    path("challenge/flag/", views.enter_challenge_flag, name="enter_challenge_flag")
]