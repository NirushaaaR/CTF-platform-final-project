from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

DOCKER_MAX_INSTANCE = 14

# Create your models here.
class DockerWeb(models.Model):
    docker_url = models.CharField(max_length=255)
    port = models.PositiveIntegerField(
        validators=(MinValueValidator(1024), MaxValueValidator(65535)), unique=True
    )
    is_deployed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.docker_url