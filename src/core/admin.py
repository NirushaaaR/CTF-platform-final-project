from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from core.models import Room, Tag, Task, TaskHint


class TaskHintInline(NestedStackedInline):
    model = TaskHint
    extra = 1


class TaskInline(NestedStackedInline):
    model = Task
    extra = 0
    inlines = (TaskHintInline,)


@admin.register(Room)
class RoomAdmin(NestedModelAdmin):
    list_display = ("title", "is_active",)
    list_editable = ("is_active",)
    inlines = (TaskInline,)

    class Media:
        js = ("js/tinyInject.js",)


admin.site.register(Tag)