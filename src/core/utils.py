from django.shortcuts import redirect
from django.utils.http import is_safe_url
from django.conf import settings
from django.db.models import Q

from core.models import Room, Task, UserAnsweredTask, UserParcitipation


def redirect_after_login(request):
    nxt = request.GET.get("next", None)
    if not(nxt is None or not is_safe_url(
        nxt, {request.get_host()}, require_https=request.is_secure()
    )):
        try:
            return redirect(nxt)
        except Exception as err:
            print(err, type(err))
    
    return redirect(settings.LOGIN_REDIRECT_URL)


def check_unfinish_prerequisites(user, room_id):
    """ check if user pass all the pass_prerequisites to enter the room """
    user_finished_room = UserParcitipation.objects.filter(
        Q(user=user), ~Q(finished_at=None)
    ).values_list("room_id", flat=True)

    unfinished_rooms = Room.objects.filter(
        Q(next_rooms=room_id), ~Q(id__in=user_finished_room)
    )

    return unfinished_rooms


def clear_all_tasks(user, room_id):
    """ check if the user clear every task in the room """
    answered_tasks_id = UserAnsweredTask.objects.filter(user=user).values_list(
        "task_id", flat=True
    )
    has_unfinished_tasks = Task.objects.filter(
        Q(room=room_id), ~Q(id__in=answered_tasks_id)
    ).exists()
    return not has_unfinished_tasks


def already_participate(user, room_id):
    """ check if user already participated in the room """
    return UserParcitipation.objects.filter(user=user, room=room_id).exists()