from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login


from core.models import Room, Task
from utils.user_check import pass_prerequisites, already_participate


def index(request):
    """ The Fist page. Will Get Rooms and shows a paginated result """
    rooms = Room.objects.all().order_by("created_at")
    context = {"rooms": rooms}

    if request.user.is_authenticated:
        participated_room = rooms.filter(participants=request.user).values_list(
            "id", "userparcitipation__finished_at"
        )
        context["user_participated"] = {k: v for k, v in participated_room}

    return render(request, "core/index.html", context)


def room(request, pk):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect_to_login(request.path)
        if pass_prerequisites(request.user, pk):
            request.user.participated_rooms.add(pk)
        else:
            print("need to do prerequire room first")
        return redirect("room", pk=pk)
    else:
        try:
            room = Room.objects.prefetch_related("tasks__hints").get(pk=pk)
            tasks = room.tasks.all()
            hints = {}
            for t in tasks:
                hints[t.task_number] = t.hints.all()
            context = {
                "room": room,
                "tasks": tasks,
                "hints": hints,
            }

            if request.user.is_authenticated:
                user_answered_tasks = tasks.filter(
                    answered_users=request.user
                ).values_list("task_number", "useransweredtask__answered_at")
                context["user_answered_tasks"] = {k: v for k, v in user_answered_tasks}

            return render(request, "core/room.html", context)
        except Room.DoesNotExist:
            raise Http404


@login_required
@require_POST
def enter_flag(request, room_id):
    if not already_participate(request.user, room_id):
        messages.warning(request, "Participate first before enter the flag")
    else:
        task_id = request.POST.get("task_id")
        flag = request.POST.get("flag")

        task = Task.objects.get(id=task_id)
        if task.flag == flag:
            messages.success(request, "Correct Flag!!")
            task.answered_users.add(request.user.id)
        else:
            messages.error(request, "Wrong Flag!!")

    # return render(request, "core/debug.html")
    return redirect("room", pk=room_id)


def admin_create_room(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    return render(request, 'core/create_room.html')