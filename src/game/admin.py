from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from game.models import Game, Challenge, ChallengeFlag


class ChallengeFlagInline(NestedStackedInline):
    model = ChallengeFlag
    extra = 1


class ChallengeInline(NestedStackedInline):
    model = Challenge
    extra = 0
    inlines = (ChallengeFlagInline,)


@admin.register(Game)
class GameAdmin(NestedModelAdmin):
    list_display = ("title", "start", "end")
    inlines = (ChallengeInline,)

    prepopulated_fields = {"slug": ("title",)}

    class Media:
        js = ("js/tinyinject.js",)