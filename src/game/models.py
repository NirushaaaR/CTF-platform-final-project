from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from docker_instance.models import DockerWeb


class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()

    is_archive = models.BooleanField(default=False)
    participants = models.ManyToManyField(
        get_user_model(),
        through="UserParticipateGame",
        blank=True,
        related_name="participated_games",
    )

    def get_absolute_url(self):
        return reverse("game", args=[str(self.slug)])

    def __str__(self) -> str:
        return self.title


class GamePeriod(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()

    game = models.OneToOneField(Game, on_delete=models.CASCADE, related_name="period")

    def get_remaining_time_percentage(self):
        rest = self.end - timezone.now()
        total = self.end - self.start
        time_percentage = rest.total_seconds() / total.total_seconds()
        return max(time_percentage, 0)
    
    def is_game_end(self):
        return timezone.now() > self.end

    def clean(self):
        if self.start >= self.end:
            raise ValidationError({"start": _("start ต้องเป็นเวลาก่อน end")})

    def __str__(self):
        return f"{self.start} - {self.end}"


class Challenge(models.Model):
    docker = models.ForeignKey(
        DockerWeb,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="challenges",
    )
    description = models.TextField()

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="challenges")


class ChallengeFlag(models.Model):
    name = models.CharField(max_length=255)
    flag = models.CharField(max_length=255, unique=True)
    explanation = models.CharField(max_length=255)
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
    participated_user = models.ForeignKey(
        UserParticipateGame, on_delete=models.PROTECT, related_name="records"
    )
    challenge = models.ForeignKey(Challenge, on_delete=models.DO_NOTHING)
    challenge_flag = models.ForeignKey(ChallengeFlag, on_delete=models.DO_NOTHING)
    answered_at = models.DateTimeField(auto_now_add=True)

    points_gained = models.PositiveIntegerField()