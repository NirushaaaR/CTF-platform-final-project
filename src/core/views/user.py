from django.db.models.aggregates import Sum
from django.db.models import F
from django.shortcuts import render, redirect

from core.models import ScoreHistory, UserParcitipation


def profile(request):
    parcitipations = UserParcitipation.objects.filter(user=request.user).select_related(
        "room"
    )
    context = {"parcitipations": parcitipations}
    return render(request, "core/profile.html", context)


def scoreboard(request):
    # top_10_users = User.objects.all().order_by("-score").va[:10]
    top10 = (
        ScoreHistory.objects.values(username=F("user__username"))
        .annotate(score=Sum("gained"))
        .order_by("-score")
    )
    context = {"top_10": top10}
    return render(request, "core/scoreboard.html", context)