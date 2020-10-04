from django.shortcuts import render

from .models import Room

def index(request):
    """ The Fist page. Will Get Rooms and shows a paginated result """
    rooms = Room.objects.all().order_by("created_at")
    context = {
        "rooms": rooms
    }
    return render(request, "core/index.html", context)