from django.db.models import F
from django.db.models.signals import m2m_changed, post_save
from django.utils import timezone
from django.dispatch.dispatcher import receiver

from core.models import Task, User, UserParcitipation, Room, ScoreHistory
from core.utils import clear_all_tasks


@receiver(m2m_changed, sender=Task.answered_users.through)
def user_clear_tasks(sender, instance, action, model, pk_set, **kwargs):
    if action == "post_add" and len(pk_set) == 1:
        # update user score by task point
        user_id = pk_set.pop()
        ScoreHistory.objects.create(
            gained=instance.points,
            type="task",
            object_id=instance.id,
            group_id=instance.room_id,
            user_id=user_id,
        )

        # check if user clear all room
        if clear_all_tasks(user_id, instance.room_id):
            UserParcitipation.objects.filter(
                user=user_id, room=instance.room_id
            ).update(finished_at=timezone.now())


@receiver(m2m_changed, sender=Room.prerequisites.through)
def add_room_prerequisites(sender, instance, action, pk_set, **kwargs):
    if action == "pre_add":
        if instance.id in pk_set:
            raise ValueError("Room Can't prerequisite itself")


@receiver(post_save, sender=ScoreHistory)
def user_get_score(sender, instance, created, **kwargs):
    if created:
        user_id = instance.user_id
        User.objects.filter(id=user_id).update(score=F('score')+instance.gained)