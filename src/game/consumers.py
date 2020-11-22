import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import F

from game.models import UserParticipateGame, UserChallengeRecord


@database_sync_to_async
def get_participants_score(game_id, user_id):
    top10 = UserParticipateGame.objects.filter(game_id=game_id).order_by("-game_score")[
        :10
    ]

    participate_id = top10.union(
        UserParticipateGame.objects.filter(user_id=user_id)
    ).values_list("id", flat=True)

    score = (
        UserChallengeRecord.objects.filter(participated_user_id__in=participate_id)
        .values(
            "points_gained",
            "answered_at",
            username=F("participated_user__user__username"),
        )
        .order_by("answered_at")
    )

    return tuple(score)


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

        # get all users score...
        await self.get_score({"type": "initiate score"})

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "update_score":
            await self.channel_layer.group_send(
                self.game_group_name, {"type": "get_score"}
            )

    async def get_score(self, event):
        # send an initial score
        data = await get_participants_score(self.game_id, self.scope["user"].id)
        await self.send(
            text_data=json.dumps(
                {"data": data, "type": "get_score"},
                default=datetime_json_converter,
            )
        )
