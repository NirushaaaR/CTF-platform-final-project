import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import F

from game.models import UserChallengeRecord


@database_sync_to_async
def get_all_participants_score(game_id):
    return tuple(
        UserChallengeRecord.objects.filter(participated_user__game_id=game_id).values(
            "points_gained",
            "answered_at",
            username=F("participated_user__user__username"),
        ).order_by("answered_at")
    )


def datetime_json_converter(obj):
    if isinstance(obj, datetime):
        return str(obj)


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.game_group_name = "game_%s" % self.game_id

        # Join room group
        await self.channel_layer.group_add(self.game_group_name, self.channel_name)

        await self.accept()
        await self.channel_layer.group_send(
            self.game_group_name,
            {
                "type": "update_score",
            },
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        await self.channel_layer.group_send(self.game_group_name, text_data_json)

    async def update_score(self, event):
        # send an initial score
        participants = await get_all_participants_score(self.game_id)

        await self.send(
            text_data=json.dumps(
                {"data": participants, "type": "update_score"},
                default=datetime_json_converter,
            )
        )
