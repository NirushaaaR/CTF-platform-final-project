from django.db.models.aggregates import Sum
from django.db.models import F
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from core.models import ScoreHistory, UserParcitipation

@login_required
def profile(request):
    parcitipations = UserParcitipation.objects.filter(user=request.user).select_related(
        "room"
    )
    context = {"parcitipations": parcitipations}
    return render(request, "core/profile.html", context)


def scoreboard(request):
    users = (
        ScoreHistory.objects.values(username=F("user__username"))
        .annotate(score=Sum("gained"))
        .order_by("-score")
    )
    context = {"users": users}
    return render(request, "core/scoreboard.html", context)