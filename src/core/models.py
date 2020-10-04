from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


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

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class Room(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    conclusion = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    prerequisites = models.ManyToManyField(
        "self", symmetrical=False, blank=True, related_name="next_rooms"
    )
    participants = models.ManyToManyField(
        get_user_model(),
        through="UserParcitipation",
        blank=True,
        related_name="participated_rooms",
    )

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
        get_user_model(),
        through="UserAnsweredTask",
        blank=True,
        related_name="cleared_tasks",
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
