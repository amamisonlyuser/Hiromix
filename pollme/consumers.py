import json
from channels.generic.websocket import AsyncWebsocketConsumer
from polls.models import Comment , Poll
from django.utils import timezone
from datetime import datetime
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async

from channels.generic.websocket import AsyncWebsocketConsumer
import json

from channels.generic.websocket import AsyncWebsocketConsumer
import json

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.poll_id = self.scope['url_route']['kwargs']['poll_id']
        self.room_group_name = 'poll_%s' % self.poll_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
     text_data_json = json.loads(text_data)
     comment = text_data_json['comment']
     username = self.scope['user'].username
     date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      
     poll = await database_sync_to_async(Poll.objects.get)(pk=self.poll_id)

     comments = Comment(
        text = comment,
        user = self.scope['user'],
         poll=poll,
     )
     await database_sync_to_async(comments.save)()
    # Send message to room group
     await self.channel_layer.group_send(
        self.room_group_name,
        {
            'type': 'poll_comment',
            'comment': comment,
            'username': username,
            'date': date,
        }
    )
    async def poll_comment(self, event):
     comment = event['comment']
     username = event['username']
     date = event['date']

    # Send message to WebSocket
     await self.send(text_data=json.dumps({
        'comment': comment,
        'username': username,
        'date': date,
    }))

