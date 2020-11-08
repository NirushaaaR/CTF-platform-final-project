from django.db import models
from django.urls import reverse


class Game(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()

    def get_absolute_url(self):
        return reverse("game", args=[str(self.slug)])

    def __str__(self) -> str:
        return self.title


class Challenge(models.Model):
    docker = models.CharField(max_length=255)
    url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
