from django.db.models import F, Subquery, Count
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from game.models import (
    Challenge,
    ChallengeFlag,
    Game,
    UserChallengeRecord,
    UserParticipateGame,
)
from core.models import ScoreHistory


def populate_game_challenges(game, user_id):
    challenges = tuple(Challenge.objects.filter(game=game).order_by("id").values())
    user_flags = tuple(
        UserChallengeRecord.objects.filter(
            participated_user__user_id=user_id, participated_user__game=game
        )
        .values(
            "challenge",
        )
        .annotate(cleared_flag=Count("challenge"))
        .order_by("challenge")
    )

    for idx, challenge in enumerate(challenges):
        challenge["cleared_flag"] = (
            user_flags[idx]["cleared_flag"] if idx < len(user_flags) else 0
        )

    return {"game": game, "challenges": challenges}


def update_score_process(game, remaingin_time, flag, user_id):
    already_answered = UserChallengeRecord.objects.filter(
        participated_user__user_id=user_id, participated_user__game=game, challenge_flag=flag
    ).exists()

    if already_answered:
        return JsonResponse({"message": "Already Enter That Flag", "correct": False})
    else:
        points_gained = (flag.point * remaingin_time) // 1
        participation = UserParticipateGame.objects.filter(user=user_id, game=game)
        UserChallengeRecord.objects.create(
            participated_user_id=Subquery(participation.values("id")),
            challenge=flag.challenge,
            challenge_flag=flag,
            points_gained=points_gained,
        )

        # add score
        participation.update(game_score=F("game_score") + points_gained)
        ScoreHistory.objects.create(
            gained=points_gained,
            type="challenge",
            object_id=flag.id,
            group_id=game.id,
            user_id=user_id,
        )
        return JsonResponse(
            {
                "message": "Right Flag",
                "correct": True,
                "points_gained": points_gained,
            }
        )


def index(request):
    games = Game.objects.all()
    context = {"games": games}
    return render(request, "game/index.html", context)


@login_required
def game_view(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    remaining_time = game.get_remaining_time_percentage()

    if remaining_time > 0:
        # game ongoing...
        game.participants.add(request.user)
    elif not game.is_archive:
        # game end and not is_archive
        # should denied the access
        pass
    else:
        # is_archive can do it but not record the participation
        pass

    context = populate_game_challenges(game, request.user.id)
    return render(request, "game/game.html", context)


@login_required
@require_POST
def enter_challenge_flag(request):
    flag = request.POST.get("flag")
    challenge_id = request.POST.get("challenge_id")

    try:
        right_flag = ChallengeFlag.objects.select_related("challenge__game").get(
            challenge_id=challenge_id, flag__iexact=flag
        )

        game = right_flag.challenge.game
        remaingin_time = game.get_remaining_time_percentage()

        if remaingin_time < 0:
            # games already ends...
            pass
        else:
            return update_score_process(
                game, remaingin_time, right_flag, request.user.id
            )

    except ChallengeFlag.DoesNotExist:
        return JsonResponse({"message": "Wrong flag", "correct": False})
