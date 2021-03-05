from django.db.models.aggregates import Sum
from django.db.models import F, Prefetch
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from core.models import ScoreHistory, UserParcitipation, Room, Task

User = get_user_model()

@login_required
def profile(request):
    parcitipations = UserParcitipation.objects.filter(user=request.user).select_related(
        "room"
    ).prefetch_related(Prefetch("room__tasks", queryset=Task.objects.order_by('task_number'), to_attr="room_tasks"))
    context = {"parcitipations": parcitipations}

    score_history = ScoreHistory.objects.filter(user_id=request.user.id, type="task").values()
    # get rooms
    task_score = {int(s["object_id"]): s["gained"] for s in score_history}

    context["task_score"] = task_score
    return render(request, "core/profile.html", context)


def scoreboard(request):
    users = User.objects.order_by('-score')
    context = {"users": users}
    return render(request, "core/scoreboard.html", context)