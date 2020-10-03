from django.db import models
from django.contrib.auth import get_user_model


class Room(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    conclusion = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prerequisites = models.ManyToManyField("self", blank=True)
    participants = models.ManyToManyField(get_user_model(), through="UserParcitipation", blank=True)


class UserParcitipation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    participated_at = models.DateTimeField(auto_now_add=True)
    is_finish = models.BooleanField(default=False)
    finished_at = models.DateTimeField(null=True, blank=True)


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    flag = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    answered_users = models.ManyToManyField(
        get_user_model(), through="UserAnsweredTask", blank=True
    )


class UserAnsweredTask(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answered_at = models.DateTimeField(auto_now_add=True)


class TaskHint(models.Model):
    hint = models.CharField(max_length=255)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
