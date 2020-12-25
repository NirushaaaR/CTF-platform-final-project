from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.forms import ModelForm

from game.models import Game, Challenge, ChallengeFlag, GamePeriod

class GameForm(ModelForm):
    class Meta:
        model = Game
        exclude = ("id",)

class ChallengeFlagInline(NestedStackedInline):
    model = ChallengeFlag
    extra = 1


class ChallengeInline(NestedStackedInline):
    model = Challenge
    extra = 0
    inlines = (ChallengeFlagInline,)


class GamePeriodInline(NestedStackedInline):
    model = GamePeriod
    extra = 0

@admin.register(Game)
class GameAdmin(NestedModelAdmin):
    list_display = ("title", "is_archive")
    inlines = (ChallengeInline, GamePeriodInline)

    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = ("js/tinyinject.js",)