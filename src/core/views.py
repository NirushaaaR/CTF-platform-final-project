from django.contrib.auth import get_user_model
from django.http.response import Http404
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.views import redirect_to_login

from django.utils import timezone

from django.conf import settings

from .models import Room, Task, UserParcitipation
from utils.user_check import pass_prerequisites, clear_all_tasks, already_participate
from utils.redirect_check import redirect_after_login


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
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_exists = (
            get_user_model()
            .objects.filter(Q(username=username) | Q(email=email))
            .exists()
        )
        if user_exists:
            print("can't use the username or password")
            return redirect("register")

        user = get_user_model().objects.create_user(
            username=username, email=email, password=password
        )
        auth.login(request, user)
        return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return render(request, "core/register.html")


@require_POST
def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required
@require_POST
def enter_flag(request, room_id):
    if not already_participate(request.user, room_id):
        print("Error user not participated can't enter flag")
    else:
        task_id = request.POST.get("task_id")
        flag = request.POST.get("flag")

        is_correct = Task.objects.filter(pk=task_id, flag=flag).exists()
        if is_correct:
            print("user get the right flag")
            request.user.cleared_tasks.add(task_id)
            if clear_all_tasks(request.user, room_id):
                UserParcitipation.objects.filter(
                    user=request.user, room=room_id
                ).update(finished_at=timezone.now())
                print("user cleared room")
        else:
            print("user get wrong tasks")

    # return render(request, "core/debug.html")
    return redirect("room", pk=room_id)
