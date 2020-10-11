from django.shortcuts import render, redirect

from core.models import User, UserParcitipation


def profile(request):
    parcitipations = UserParcitipation.objects.filter(user=request.user).select_related("room")
    context = {"parcitipations": parcitipations}
    return render(request, "core/profile.html", context)


def scoreboard(request):
    top_10_users = User.objects.all().order_by("-score")[:10]
    context = {"top_10": top_10_users}
    return render(request, "core/scoreboard.html", context)