import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.game_name = self.scope["url_route"]["kwargs"]["game_slug"]
        self.game_group_name = "game_%s" % self.game_name

        # Join room group
        await self.channel_layer.group_add(self.game_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # Send message to room group
        await self.channel_layer.group_send(
            self.game_group_name,
            text_data_json,
        )

    # Receive message from room group
    async def answer_flag(self, event):
        flag = event["data"]["flag"]

        # check flag
        print(flag)
