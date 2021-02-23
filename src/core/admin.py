from django.contrib import admin
from django.db import models
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from markdownx.widgets import AdminMarkdownxWidget

from core.models import Room, Tag, Task, TaskHint, User, RoomContent


class TaskHintInline(NestedStackedInline):
    model = TaskHint
    extra = 1


class TaskInline(NestedStackedInline):
    model = Task
    extra = 1
    inlines = (TaskHintInline,)
    
    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


class RoomContentInline(NestedStackedInline):
    model = RoomContent
    extra = 1

    formfield_overrides = {
        models.TextField: {'widget': AdminMarkdownxWidget},
    }


@admin.register(Room)
class RoomAdmin(NestedModelAdmin):
    list_display = ("title", "preview", "is_active", "created_at", "updated_at")
    list_editable = ("is_active",)
    inlines = (RoomContentInline, TaskInline,)

    class Media:
        css = {
            'all': ('css/markdown.css', ),
        }
        js = ("js/jquery.js", "js/popper.min.js", "js/bootstrap.min.js",)

    #class Media:
    #    js = ("js/tinyinject.js",)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("id",)
    list_display = ("email", "username", "score", "is_superuser", "is_staff")
    list_editable = ("is_superuser", "is_staff")

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        (_("Personal info"), {"fields": ("score",)}),
        (_("Permission"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Importent dates"), {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "room")
    class Media:
        js = ("js/tinyinject.js",)

admin.site.register(Tag)
