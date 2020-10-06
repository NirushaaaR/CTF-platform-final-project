from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from core.models import Room, Task, TaskHint


class TaskHintInline(NestedStackedInline):
    model = TaskHint
    extra = 1


class TaskInline(NestedStackedInline):
    model = Task
    extra = 0
    inlines = (TaskHintInline,)


@admin.register(Room)
class RoomAdmin(NestedModelAdmin):
    inlines = (TaskInline,)
