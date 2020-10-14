from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core.models import Room, Tag, Task, TaskHint, User


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

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ('id',)
    list_display = ('email', 'username', 'score', 'is_superuser')
    list_editable = ('is_superuser',)

    fieldsets = ((None, {
        'fields': ('username', 'email', 'password')
    }), (_("Personal info"), {
        'fields': ('score', )
    }), (_("Permission"), {
        'fields': ('is_active', 'is_staff', 'is_superuser')
    }), (_("Importent dates"), {
        'fields': ('last_login', )
    }))

    add_fieldsets = ((None, {
        'classes': ('wide', ),
        'fields': ('username', 'email', 'password1', 'password2')
    }), )


admin.site.register(Tag)