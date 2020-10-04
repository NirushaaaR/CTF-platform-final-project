from django.shortcuts import render, get_object_or_404

from .models import Room

def index(request):
    """ The Fist page. Will Get Rooms and shows a paginated result """
    rooms = Room.objects.all().order_by("created_at")
    context = {
        "rooms": rooms
    }
    return render(request, "core/index.html", context)

def room(request, room_id):
    """when click to see a room shows room information tasks and hints 
    if user still not participate room let user participate but check the prerequsuite first
    if room is done show conclusion"""
    room = get_object_or_404(Room, pk=room_id)

    # get all tasks in room
    tasks = room.tasks.all().order_by("task_number")
    hints = {}
    for task in tasks:
        hints[task.task_number] = task.hints.all()

    context = {
        "room": room,
        "tasks": tasks,
        "hints": hints,
    }

    print(hints)
    return render(request, "core/room.html", context)