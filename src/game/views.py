from datetime import datetime
from django.contrib import messages

from django.db.models import F, Subquery, Count, Q
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from game.models import (
    Challenge,
    ChallengeFlag,
    Game,
    UserChallengeRecord,
    UserParticipateGame,
)

from core.models import ScoreHistory, User


def populate_game_challenges(game, user_id):
    challenges = tuple(
        Challenge.objects.filter(game=game)
        .prefetch_related("flags")
        .annotate(
            docker_image=F("docker__docker"),
            url=F("docker__url"),
        )
    )

    # find all cleared flags
    user_records = UserChallengeRecord.objects.filter(
        challenge__in=challenges, participated_user__user_id=user_id
    )
    flags = []
    for c in challenges:
        for flag in c.flags.all():
            # find if user already answer the flag
            flag.status = "Not Solved " + "\u2715"
            flag.answered = False
            for record in user_records:
                if record.challenge_flag_id == flag.id:
                    flag.status = "Solved "+ "\u2713"
                    flag.answered = True
                    flag.points_gained = record.points_gained
                    break
            flags.append(flag)

    return {"game": game, "challenges": challenges, "flags": flags}


def update_score_process(game, flag, user_id, username):
    already_answered = UserChallengeRecord.objects.filter(
        participated_user__user_id=user_id,
        participated_user__game=game,
        challenge_flag=flag,
    ).exists()

    if already_answered:
        return {"message": "ตอบ flag นี้ไปแล้ว", "correct": False}
    else:
        points_gained = flag.point

        try:
            if game.period:
                remaingin_time = game.period.get_remaining_time_percentage()
                points_gained = round(points_gained * remaingin_time)
        except Game.period.RelatedObjectDoesNotExist:
            pass

        participation = UserParticipateGame.objects.filter(user=user_id, game=game)
        user_challenges_record = UserChallengeRecord(
            participated_user_id=Subquery(participation.values("id")),
            challenge=flag.challenge,
            challenge_flag=flag,
            points_gained=points_gained,
        )
        user_challenges_record.save()

        # add score
        participation.update(game_score=F("game_score") + points_gained)
        ScoreHistory.objects.create(
            gained=points_gained,
            type="challenge",
            object_id=flag.id,
            group_id=game.id,
            user_id=user_id,
        )

        return {
            "message": "ถูกต้อง",
            "correct": True,
            "points_gained": points_gained,
            "answered_at": user_challenges_record.answered_at,
            "flagid": user_challenges_record.challenge_flag_id,
        }


def get_top10_score(game_id):
    top10 = UserParticipateGame.objects.filter(game_id=game_id).order_by("-game_score").values_list("id", flat=True)[:10]

    score = (
        UserChallengeRecord.objects.filter(participated_user_id__in=top10)
        .values(
            "points_gained",
            "answered_at",
            username=F("participated_user__user__username"),
        )
        .order_by("answered_at")
    )

    return tuple(score)


def index(request):
    now = datetime.now()
    games = Game.objects.select_related("period").filter(is_archive=False)
    context = {"games": games}
    return render(request, "game/index.html", context)


@login_required
def game_view(request, game_slug):
    game = get_object_or_404(Game.objects.select_related("period"), slug=game_slug)

    try:
        remaining_time = game.period.get_remaining_time_percentage()
        if remaining_time > 1:
            messages.warning(request, "ยังไม่ถึงเวลาเริ่มเกม")
            return redirect('game_index')
        game.participants.add(request.user)
    except Game.period.RelatedObjectDoesNotExist:
        # no periods game always ongoning
        game.period = None
        game.participants.add(request.user)

    context = populate_game_challenges(game, request.user.id)
    return render(request, "game/game.html", context)


@login_required
@require_POST
def enter_challenge_flag(request, game_id):
    game = get_object_or_404(Game.objects.select_related("period"), id=game_id)

    try:
        # check if game has period and started yet...
        if not game.period.is_game_start():
            return JsonResponse({"message": "เกมยังไม่เริ่ม", "correct": False})
    except Game.period.RelatedObjectDoesNotExist:
        # no periods game always ongoning
        game.period = None
    
    try:
        right_flag = ChallengeFlag.objects.select_related("challenge").get(
            flag__iexact=request.POST.get("flag", "").strip(), challenge__game_id=game_id
        )
        result = update_score_process(
            game, right_flag, request.user.id, request.user.username
        )
        return JsonResponse(result)

    except ChallengeFlag.DoesNotExist:
        return JsonResponse({"message": "ผิด", "correct": False})
    
    


@login_required
def get_current_top10_score(request, game_id):
    scores = get_top10_score(game_id)
    return JsonResponse({"data": scores})