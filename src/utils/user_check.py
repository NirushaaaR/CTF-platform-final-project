from django.db.models import Q

from core.models import Room, Task, UserAnsweredTask, UserParcitipation


def pass_prerequisites(user, room_id):
    user_finished_room = UserParcitipation.objects.filter(
        Q(user=user), ~Q(finished_at=None)
    ).values_list("room_id", flat=True)

    have_unfinished_room = Room.objects.filter(
        Q(next_rooms=room_id), ~Q(id__in=user_finished_room)
    ).exists()

    return not have_unfinished_room


def clear_all_tasks(user, room_id):
    answered_tasks = UserAnsweredTask.objects.filter(user=user)
    has_unfinished_tasks = Task.objects.filter(
        Q(room=room_id), ~Q(id__in=answered_tasks)
    ).exists()
    return not has_unfinished_tasks


def already_participate(user, room_id):
    return UserParcitipation.objects.filter(user=user, room=room_id).exists()