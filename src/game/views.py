from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Game


def index(request):
    games = Game.objects.all()
    context = {"games": games}
    return render(request, "game/index.html", context)


@login_required
def game_view(request, game_slug):
    game = get_object_or_404(
        Game.objects.prefetch_related("challenges"), slug=game_slug
    )

    context = {"game": game}
    game.participants.add(request.user)

    return render(request, "game/game.html", context)