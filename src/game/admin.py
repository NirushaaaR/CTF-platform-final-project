from django.contrib import admin
from django.forms import ModelForm
from django.db import models

from nested_admin import NestedStackedInline, NestedModelAdmin
from markdownx.widgets import AdminMarkdownxWidget

from game.models import Game, Challenge, ChallengeFlag, GamePeriod, UserChallengeRecord


class ChallengeFlagInline(NestedStackedInline):
    model = ChallengeFlag
    extra = 1


class ChallengeInline(NestedStackedInline):
    model = Challenge
    extra = 0
    inlines = (ChallengeFlagInline,)

    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }


class GamePeriodInline(NestedStackedInline):
    model = GamePeriod
    extra = 0


@admin.register(Game)
class GameAdmin(NestedModelAdmin):
    list_display = ("title", "is_archive")
    inlines = (ChallengeInline, GamePeriodInline)

    formfield_overrides = {
        models.TextField: {"widget": AdminMarkdownxWidget},
    }

    prepopulated_fields = {"slug": ("title",)}

    class Media:
        css = {
            "all": ("css/markdown.css",),
        }


@admin.register(UserChallengeRecord)
class UserChallengeRecordAdmin(admin.ModelAdmin):
    list_display = ("answered_at", "challenge", "challenge_flag")