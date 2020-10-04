from os import name
from django.urls import path

from .views import index, room

urlpatterns = [
    path("", index, name="index"),
    path("room/<int:room_id>", room, name="room")
]
