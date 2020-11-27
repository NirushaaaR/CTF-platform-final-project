# chat/urls.py
from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_instance, name="create_docker_instance"),
]