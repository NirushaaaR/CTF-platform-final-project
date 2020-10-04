from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.http import is_safe_url
from django.db.models import Q
from django.contrib.auth.views import redirect_to_login

from django.conf import settings

from .models import Room, UserParcitipation


def index(request):
    """ The Fist page. Will Get Rooms and shows a paginated result """
    rooms = Room.objects.all().order_by("created_at")
    context = {"rooms": rooms}
    return render(request, "core/index.html", context)


def room(request, pk):
    """when click to see a room shows room information tasks and hints
    if user still not participate room let user participate but check the prerequsuite first
    if room is done show conclusion"""
    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect_to_login(request.path)

        user_finished_room = UserParcitipation.objects.filter(
            Q(user=request.user), ~Q(finished_at=None)
        ).values_list("room_id", flat=True)

        not_finish_prerequisites = Room.objects.filter(
            Q(next_rooms=pk), ~Q(id__in=user_finished_room)
        )

        print(not_finish_prerequisites)
        if len(not_finish_prerequisites) > 0:
            print("need to do room")
            print(not_finish_prerequisites)
        else:
            print("all finish can begin works now")
        return HttpResponse("ONGoing")
    else:
        # get all tasks in room
        room = get_object_or_404(Room, pk=pk)
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
