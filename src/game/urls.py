# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="game_index"),
    path("<str:game_slug>/", views.game_view, name="game"),
    path("score/<str:game_id>", views.get_current_top10_score, name="game_score"),
    path("challenge/flag/", views.enter_challenge_flag, name="enter_challenge_flag")
]