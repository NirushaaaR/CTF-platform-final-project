import json
from datetime import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.db.models import F

from game.models import UserParticipateGame, UserChallengeRecord


def map_user_score_data(users, score):
    mapping = []

    for u in users:
        user_dict = {"username": u["username"], "score": []}
        for s in score:
            if u["id"] == s.participated_user_id:
                user_dict["score"].append(
                    {"date": s.answered_at, "points_gained": s.points_gained}
                )
        mapping.append(user_dict)

    return mapping


@database_sync_to_async
def get_all_participants_score(game_id, user_id):
    top10 = (
        UserParticipateGame.objects.filter(game_id=game_id)
        .order_by("-game_score")
        .values("id", "user_id", username=F("user__username"))[:10]
    )
    all_user = top10.union(
        UserParticipateGame.objects.filter(user=user_id).values(
            "id", "user_id", username=F("user__username")
        )
    )

    score = UserChallengeRecord.objects.filter(
        participated_user_id__in=[u["id"] for u in all_user]
    )

    return map_user_score_data(all_user, score)


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

        data = await get_all_participants_score(self.game_id, self.scope["user"].id)
        await self.send(
            text_data=json.dumps(
                {"data": data, "type": "initial_score"},
                default=datetime_json_converter,
            )
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
        start = datetime.now()
        # participants = await get_all_participants_score(self.game_id, self.scope['user'].id)
        end = datetime.now()

        print("time usage", (end - start).total_seconds())

        await self.send(
            text_data=json.dumps(
                {
                    # "data": participants,
                    "type": "update_score"
                },
                default=datetime_json_converter,
            )
        )
