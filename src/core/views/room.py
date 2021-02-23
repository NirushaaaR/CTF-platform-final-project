from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F
from django.utils import timezone

from markdownx.utils import markdownify

from core.models import Room, Task, RoomContent, UserAnsweredTask, ScoreHistory, UserParcitipation
from core.utils import already_participate, clear_all_tasks


def query_paginated_room(request, rooms):
    search = request.GET.get("search")
    if search:
        rooms = rooms.filter(
            Q(title__icontains=search)
            | Q(preview__icontains=search)
            | Q(description__icontains=search)
        )
    pagination = Paginator(rooms, 6)
    current_page = request.GET.get("page", 1)

    context = {"rooms": pagination.get_page(current_page), "search": search}
    if request.user.is_authenticated:
        participated_room = rooms.filter(participants=request.user).values_list(
            "id", "userparcitipation__finished_at"
        )
        context["user_participated"] = {k: v for k, v in participated_room}
    return context


def index(request):
    """ The Fist page. Will Get Rooms and shows a paginated result """
    rooms = (
        Room.objects.prefetch_related("tags")
        .filter(is_active=True)
        .order_by("created_at")
    )
    context = query_paginated_room(request, rooms)
    return render(request, "core/index.html", context)


def room_by_tag(request, tag):
    rooms = (
        Room.objects.prefetch_related("tags")
        .filter(is_active=True, tags__name=tag)
        .order_by("created_at")
    )
    context = query_paginated_room(request, rooms)
    return render(request, "core/index.html", context)


@login_required
def room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    tasks = (
        Task.objects.filter(room=room)
        .select_related("docker")
        .prefetch_related("hints")
        .order_by("task_number")
    )
    contents = RoomContent.objects.filter(room=room).order_by("content_number")

    context = {
        "room": room,
        "tasks": tasks,
        "contents": contents,
        "contents_count": contents.count(),
        "tasks_count": tasks.count(),
    }

    if request.user.is_authenticated:
        user_answered_tasks = tasks.filter(answered_users=request.user).values_list(
            "task_number", "useransweredtask__answered_at"
        )
        context["user_answered_tasks"] = {k: v for k, v in user_answered_tasks}
        context["is_finish"] = context["tasks_count"] == len(user_answered_tasks)

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
    task = get_object_or_404(Task, id=task_id)

    if task.flag == flag or task.flag is None:
        task.answered_users.add(request.user.id)
        return JsonResponse({"message": "ถูกต้อง!!", "conclusion": markdownify(task.conclusion), "correct": True})
    else:
        return JsonResponse({"message": "ผิด!!", "correct": False})


@login_required
@require_POST
def unlock_conclusion(request, room_id):
    """ user unlock conclusion but won't be able to gain point """
    if not already_participate(request.user, room_id):
        request.user.participated_rooms.add(room_id)
    
    task_id = request.POST.get("task_id")
    task = get_object_or_404(Task, id=task_id)
    # check if already answered
    if UserAnsweredTask.objects.filter(user=request.user, task_id=task_id).exists():
        return JsonResponse({"message": "ตอบคำถามนี้ไปแล้ว", "unlocked": False})

    UserAnsweredTask.objects.create(user=request.user, task_id=task_id)
    ScoreHistory.objects.create(
        gained=0,
        type="task",
        object_id=task_id,
        group_id=room_id,
        user_id=request.user.id,
    )

    # check if user clear all room
    if clear_all_tasks(request.user.id, room_id):
        UserParcitipation.objects.filter(
            user_id=request.user.id, room_id=room_id
        ).update(finished_at=timezone.now())

    return JsonResponse({"message": "ปลดล็อคเฉลย", "unlocked": True, "conclusion": markdownify(task.conclusion)})

    

def admin_create_room(request):
    if not request.user.is_superuser:
        raise PermissionDenied()
    return render(request, "core/create_room.html")
