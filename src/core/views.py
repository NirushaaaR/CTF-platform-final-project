from django.http import request
from django.http.response import Http404, HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.urls.base import reverse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url
from django.db.models import Q
from django.contrib.auth.views import redirect_to_login

from django.utils import timezone

from django.conf import settings

from .models import Room, Task, UserAnsweredTask, UserParcitipation


def user_pass_prerequisites(user, room_id):
    user_finished_room = UserParcitipation.objects.filter(
        Q(user=user), ~Q(finished_at=None)
    ).values_list("room_id", flat=True)

    have_unfinished_room = Room.objects.filter(
        Q(next_rooms=room_id), ~Q(id__in=user_finished_room)
    ).exists()

    return not have_unfinished_room


def user_clear_all_tasks(user, room_id):
    answered_tasks = UserAnsweredTask.objects.filter(user=user)
    exists_unfinished_tasks = Task.objects.filter(
        Q(room=room_id), ~Q(id__in=answered_tasks)
    ).exists()
    return not exists_unfinished_tasks


def user_is_participated(user, room_id):
    return UserParcitipation.objects.filter(user=user, room=room_id).exists()


def add_participation_info(user, rooms):
    participated_room = rooms.filter(participants=user).values_list(
        "id", "userparcitipation__finished_at"
    )
    index = 0
    for r in rooms:
        if r.id == participated_room[index][0]:
            print("same match", r, participated_room[index])
            r.is_participating = True
            r.finished_at = participated_room[index][1]
            index += 1


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
        if user_pass_prerequisites(request.user, pk):
            request.user.participated_rooms.add(pk)
        else:
            print("need to do prerequire room first")
        return render(request, "core/debug.html")
    else:
        try:
            room = Room.objects.prefetch_related("tasks", "tasks__hints").get(pk=pk)
            tasks = room.tasks.all()
            hints = {}
            for t in tasks:
                hints[t.task_number] = t.hints.all()
            context = {
                "room": room,
                "tasks": tasks,
                "hints": hints,
            }
            return render(request, "core/room.html", context)
        except Room.DoesNotExist:
            raise Http404


def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    if nxt is None or not is_safe_url(
        nxt, {request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return redirect(nxt)


def login(request):
    """ login the user """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect_after_login(request)

        # wrong credentials
        redirect_to = request.path
        if request.GET.get("next"):
            redirect_to += f"?next={request.GET.get('next')}"
        return redirect(redirect_to)

    else:
        if request.user.is_authenticated:
            # user already login
            return redirect("index")
        return render(request, "core/login.html", {"next": request.GET.get("next")})


def register(request):
    if request.method == "POST":
        pass
    else:
        return render(request, "core/register.html")


# @require_POST
def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required
def secret_route(request):
    print("Enter secret route")
    return redirect("index")


@login_required
@require_POST
def enter_flag(request, room_id):
    if not user_is_participated(request.user, room_id):
        print("Error user not participated can't enter flag")
    else:
        task_id = request.POST.get("task_id")
        flag = request.POST.get("flag")

        is_correct = Task.objects.filter(pk=task_id, flag=flag).exists()
        if is_correct:
            print("user get the right flag")
            request.user.cleared_tasks.add(task_id)
            if user_clear_all_tasks(request.user, room_id):
                UserParcitipation.objects.filter(
                    user=request.user, room=room_id
                ).update(finished_at=timezone.now())
                print("user cleared room")
        else:
            print("user get wrong tasks")

    # return render(request, "core/debug.html")
    return redirect("room", pk=room_id)
