from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = "core"

    def ready(self) -> None:
        from core.signals import user_clear_tasks, add_room_prerequisites, user_get_score  # noqa
