from django.contrib import admin

from .models import Room, UserParcitipation, Task, UserAnsweredTask, TaskHint

admin.site.register(Room)
admin.site.register(UserParcitipation)
admin.site.register(Task)
admin.site.register(UserAnsweredTask)
admin.site.register(TaskHint)
