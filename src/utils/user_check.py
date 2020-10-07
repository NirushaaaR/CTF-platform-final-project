from django.db.models import Q

from core.models import Room, Task, UserAnsweredTask, UserParcitipation


def pass_prerequisites(user, room_id):
    """ check if user pass all the pass_prerequisites to enter the room """
    user_finished_room = UserParcitipation.objects.filter(
        Q(user=user), ~Q(finished_at=None)
    ).values_list("room_id", flat=True)

    have_unfinished_room = Room.objects.filter(
        Q(next_rooms=room_id), ~Q(id__in=user_finished_room)
    ).exists()

    return not have_unfinished_room


# <QuerySet [<UserAnsweredTask: nirus - Try CTF>, <UserAnsweredTask: nirus - xss1>, <UserAnsweredTask: nirus - xss2>]>
# <QuerySet [<Task: xss1>, <Task: xss2>]>
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