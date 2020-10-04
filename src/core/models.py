from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

class Room(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    conclusion = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="next_rooms")
    participants = models.ManyToManyField(get_user_model(), through="UserParcitipation", blank=True)

    def __str__(self):
        return self.title


class UserParcitipation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    participated_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.room}"


class Task(models.Model):
    task_number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=255)
    description = models.TextField()
    flag = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="tasks")

    answered_users = models.ManyToManyField(
        get_user_model(), through="UserAnsweredTask", blank=True
    )

    def __str__(self):
        return self.title


class UserAnsweredTask(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.task}"


class TaskHint(models.Model):
    hint = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="hints")

    def __str__(self):
        return self.hint
