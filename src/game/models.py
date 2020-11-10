from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    is_archive = models.BooleanField(default=False)
    participants = models.ManyToManyField(
        get_user_model(),
        through="UserParticipateGame",
        blank=True,
        related_name="participated_games",
    )

    def get_absolute_url(self):
        return reverse("game", args=[str(self.slug)])

    def get_remaining_time_percentage(self):
        rest = self.end - timezone.now()
        total = self.end - self.start
        return rest.total_seconds()/total.total_seconds()

    def __str__(self) -> str:
        return self.title


class Challenge(models.Model):
    docker = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    flag_count = models.PositiveIntegerField()

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="challenges")

    def __str__(self) -> str:
        return self.docker


class ChallengeFlag(models.Model):
    flag = models.CharField(max_length=255)
    point = models.PositiveIntegerField()

    challenge = models.ForeignKey(
        Challenge, on_delete=models.CASCADE, related_name="flags"
    )

    def __str__(self) -> str:
        return self.flag


class UserParticipateGame(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    game_score = models.IntegerField(default=0)
    participate_at = models.DateTimeField(auto_now_add=True)


class UserChallengeRecord(models.Model):
    participated_user = models.ForeignKey(UserParticipateGame, on_delete=models.PROTECT)
    challenge = models.ForeignKey(Challenge, on_delete=models.DO_NOTHING)
    challenge_flag = models.ForeignKey(ChallengeFlag, on_delete=models.DO_NOTHING)
    answered_at = models.DateTimeField(auto_now_add=True)

    points_gained = models.PositiveIntegerField()