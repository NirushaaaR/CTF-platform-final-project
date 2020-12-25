from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from core.models import Room, Task
from core.utils import already_participate


def index(request):
    """ The Fist page. Will Get Rooms and shows a paginated result """
    rooms = Room.objects.filter(is_active=True).order_by("-updated_at")
    pgination = Paginator(rooms, 6)
    current_page = request.GET.get("page", 1)
    context = {
        "rooms": pgination.get_page(current_page),
    }

    if request.user.is_authenticated:
        participated_room = rooms.filter(participants=request.user).values_list(
            "id", "userparcitipation__finished_at"
        )
        context["user_participated"] = {k: v for k, v in participated_room}

    return render(request, "core/index.html", context)


@login_required
def room(request, pk):
    room = get_object_or_404(Room.objects.select_related("docker").prefetch_related("tasks__hints"), pk=pk)
    tasks = room.tasks.all()

    context = {
        "room": room,
        "tasks": tasks,
    }

    if request.user.is_authenticated:
        user_answered_tasks = tasks.filter(answered_users=request.user).values_list(
            "task_number", "useransweredtask__answered_at"
        )
        context["user_answered_tasks"] = {k: v for k, v in user_answered_tasks}
        context["is_finish"] = len(tasks) == len(user_answered_tasks)

    return render(request, "core/room.html", context)


@login_required
@require_POST
def enter_flag(request, room_id):
    # check is Bob ?
    if request.user.username == "Bob":
        messages.warning(request, "Bob ไม่สามารถใส่ Flag ได้กรุณา Logout")
        return redirect("room", pk=room_id)

    if not already_participate(request.user, room_id):
        request.user.participated_rooms.add(room_id)

    task_id = request.POST.get("task_id")
    flag = request.POST.get("flag")
    task = Task.objects.get(id=task_id)

    if task.flag == flag:
        task.answered_users.add(request.user.id)
        return JsonResponse({"message": "ถูกต้อง!!", "correct": True})
    else:
        return JsonResponse({"message": "ผิด!!", "correct": False})


def admin_create_room(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    return render(request, "core/create_room.html")
