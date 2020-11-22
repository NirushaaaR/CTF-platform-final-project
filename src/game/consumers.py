import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import F

from game.models import UserParticipateGame, UserChallengeRecord


@database_sync_to_async
def get_top10_score(game_id):
    top10 = UserParticipateGame.objects.filter(game_id=game_id).order_by("-game_score").values_list("id", flat=True)[:10]

    score = (
        UserChallengeRecord.objects.filter(participated_user_id__in=top10)
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
        data = await get_top10_score(self.game_id)
        await self.send(
            text_data=json.dumps(
                {"data": data, "type": "get_score"},
                default=datetime_json_converter,
            )
        )

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        if text_data_json["type"] == "update_score":
            data = await get_top10_score(self.game_id)
            await self.channel_layer.group_send(
                self.game_group_name, 
                {"type": "get_score", "data": data}
            )

    async def get_score(self, event):
        # send an initial score
        await self.send(
            text_data=json.dumps(
                {"data": event['data'], "type": "get_score"},
                default=datetime_json_converter,
            )
        )
