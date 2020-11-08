from django.shortcuts import get_object_or_404
from django.shortcuts import render

from .models import Game

def index(request):
    games = Game.objects.all()
    context = {"games": games}
    return render(request, "game/index.html", context)

def game(request, game_slug):
    game = get_object_or_404(Game.objects.prefetch_related("challenges"), slug=game_slug)
    context = {"game": game}
    return render(request, "game/game.html", context)