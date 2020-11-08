# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='game_index'),
    path('<str:game_slug>/', views.game, name='game'),
]