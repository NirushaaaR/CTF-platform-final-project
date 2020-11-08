# chat/views.py
from django.http.response import HttpResponse
from django.shortcuts import render

from .models import Game

def index(request):
    games = Game.objects.all()
    context = {"games": games}
    print(games)
    return render(request, "game/index.html", context)

def game(request, game_slug):
    game = Game.objects.prefetch_related("challenges").get(slug=game_slug)
    context = {"game": game}
    return render(request, "game/game.html", context)