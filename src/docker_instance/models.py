from django.db import models

# Create your models here.
class DockerWeb(models.Model):
    name = models.CharField(max_length=255)
    docker_url = models.CharField(max_length=255)
    is_deployed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name