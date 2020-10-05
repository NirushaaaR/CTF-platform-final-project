from django.http import request
from django.shortcuts import render, redirect

from core.models import User


def profile(request):
    return render(request, "core/profile.html")


def scoreboard(request):
    top_10_users = User.objects.all().order_by("-score")[:10]
    context = {"top_10": top_10_users}
    return render(request, "core/scoreboard.html", context)