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


def index(request):
    games = Game.objects.all()
    context = {"games": games}
    return render(request, "game/index.html", context)


@login_required
def game_view(request, game_slug):
    game = get_object_or_404(Game, slug=game_slug)
    challenges = tuple(Challenge.objects.filter(game=game).order_by("id").values())

    game.participants.add(request.user)
    user_flags = tuple(
        UserChallengeRecord.objects.filter(
            participated_user__user=request.user, participated_user__game=game
        )
        .values(
            "challenge",
        )
        .annotate(cleared_flag=Count("challenge"))
        .order_by("challenge")
    )

    for idx, challenge in enumerate(challenges):
        challenge["cleared_flag"] = user_flags[idx]["cleared_flag"] if idx < len(user_flags) else 0

    context = {"game": game, "challenges": challenges}
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
        remain_time = game.get_remaining_time_percentage()

        points_gained = 0

        if remain_time > 1:
            # games already ends...
            pass
        else:

            points_gained = (right_flag.point * remain_time) // 1
            participation = UserParticipateGame.objects.filter(
                user=request.user, game=game
            )

            created = UserChallengeRecord.objects.get_or_create(
                participated_user_id=Subquery(participation.values("id")),
                challenge=right_flag.challenge,
                challenge_flag=right_flag,
                defaults={"points_gained": points_gained},
            )[1]

            if created:
                # add score
                participation.update(game_score=F("game_score") + points_gained)
                ScoreHistory.objects.create(
                    gained=points_gained,
                    type="challenge",
                    object_id=right_flag.id,
                    group_id=game.id,
                    user_id=request.user.id,
                )
                return JsonResponse(
                    {
                        "message": "Right Flag",
                        "correct": True,
                        "points_gained": points_gained,
                    }
                )
            else:
                return JsonResponse(
                    {"message": "Already Enter That Flag", "correct": False}
                )

    except ChallengeFlag.DoesNotExist:
        return JsonResponse({"message": "Wrong flag", "correct": False})
