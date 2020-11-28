from django.contrib import admin

from docker_instance.models import DockerWeb

# Register your models here.
@admin.register(DockerWeb)
class DockerAdmin(admin.ModelAdmin):
    list_display = ("docker", "port",)

    class Media:
        js = ("js/manageDocker.js",)