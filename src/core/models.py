from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from docker_instance.models import DockerWeb


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """ create and save user with email and password """
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(
            email=self.normalize_email(email), username=username, **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)  # supporting many database ?

        return user

    def create_superuser(self, username, email, password=None):
        """ create and save a superuser """
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user model that use email as username field """

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class ScoreHistory(models.Model):
    gained = models.IntegerField()
    type = models.CharField(
        max_length=9, choices=(("task", "task"), ("challenge", "challenge"))
    )
    object_id = models.CharField(max_length=255)
    group_id = models.CharField(max_length=255)
    time = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="score_history"
    )

    def __str__(self) -> str:
        return f"{self.user_id} gain {self.gained} from {self.type}"


class Room(models.Model):
    class DifficultyChoices(models.IntegerChoices):
        VERY_HARD = 5, _('Very Hard')
        HARD = 4, _('Hard')
        MEDIUM = 3, _('Medium')
        EASY = 2, _('Easy')
        VERY_EASY = 1, _('Very Easy')

    title = models.CharField(max_length=255)
    preview = models.CharField(max_length=255)
    difficulty = models.IntegerField(
        choices=DifficultyChoices.choices,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tags = models.ManyToManyField("Tag", blank=True, related_name="rooms")
    next_rooms = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="prerequisites"
    )
    participants = models.ManyToManyField(
        get_user_model(),
        through="UserParcitipation",
        blank=True,
        related_name="participated_rooms",
    )

    def get_absolute_url(self):
        return reverse("room", args=[str(self.pk)])
    
    def get_tracker_url(self):
        return reverse("user_content_tracker", args=[str(self.pk)])
    
    def get_difficulty_label(self):
        for num, text in Room.DifficultyChoices.choices:
            if num == self.difficulty:
                return text

    def __str__(self):
        return self.title


class RoomContent(models.Model):
    content_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=50)
    left = models.TextField()
    right = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="contents")

    class Meta:
        unique_together = ("content_number", "room")

    def __str__(self):
        return f"content {self.room} {self.id}"


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class UserParcitipation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    participated_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} - {self.room}"

class Task(models.Model):
    task_number = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    title = models.CharField(max_length=255)
    description = models.TextField()
    flag = models.CharField(max_length=255, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="tasks")
    points = models.PositiveIntegerField()
    docker = models.ForeignKey(
        DockerWeb,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
    )
    docker_url_path = models.CharField(max_length=100, null=True, blank=True)
    conclusion = models.TextField(null=True, blank=True)

    answered_users = models.ManyToManyField(
        get_user_model(),
        through="UserAnsweredTask",
        blank=True,
        related_name="cleared_tasks",
    )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = (("room", "task_number"),)


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
