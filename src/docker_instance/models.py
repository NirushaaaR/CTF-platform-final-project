from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse

DOCKER_MAX_INSTANCE = 14

# Create your models here.
class DockerWeb(models.Model):
    docker = models.CharField(max_length=255)
    port = models.PositiveIntegerField(
        validators=(MinValueValidator(1024), MaxValueValidator(65535)), unique=True
    )
    url = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse("docker-info", args=[str(self.id)])

    def __str__(self) -> str:
        return self.docker