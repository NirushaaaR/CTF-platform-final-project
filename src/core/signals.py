from django.db.models import F
from django.db.models.signals import m2m_changed
from django.utils import timezone
from django.dispatch.dispatcher import receiver

from core.models import Task, UserParcitipation
from utils.user_check import clear_all_tasks


@receiver(m2m_changed, sender=Task.answered_users.through)
def user_clear_tasks(sender, instance, action, model, pk_set, **kwargs):
    if action == "post_add" and len(pk_set) == 1:
        # update user score by task point
        user_id = pk_set.pop()
        model.objects.filter(pk=user_id).update(score=F("score") + instance.points)

        # check if user clear all room
        if clear_all_tasks(user_id, instance.room_id):
            print("user cleared room")
            UserParcitipation.objects.filter(
                user=user_id, room=instance.room_id
            ).update(finished_at=timezone.now())
