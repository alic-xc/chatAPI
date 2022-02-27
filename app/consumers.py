import json
from datetime import datetime

from asgiref.sync import async_to_sync, sync_to_async
from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth.models import User

from app.models import Chat, ChatRoom


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message_id = text_data_json['message_id']
        username = text_data_json['username']

        if not text_data_json.get('read'):
            message = text_data_json['message']
            room = text_data_json['room']
            message_id = text_data_json['message_id']
            time = datetime.now()
            read = False

            # Send message to room group
            async_to_sync(self.save_message)(username, room, message, message_id)

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'message_id': message_id,
                    'timestamp': str(time),
                    'read': read,
                }
            )

        else:

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message_id': message_id,
                    'username': username,
                    'read': 'true'
                }
            )

    # Receive message from room group
    def chat_message(self, event):

        read = event['read']
        message_id = event['message_id']
        username = event['username']

        if not read:
            message = event['message']
            timestamp = event['timestamp']

            self.send(text_data=json.dumps({
                'action_type': 'new',
                'message': message,
                'message_id': message_id,
                'username': username,
                'timestamp': str(timestamp),
                'read': read,
            }))

        else:

            self.send(text_data=json.dumps({
                'action_type': 'update',
                'read': True,
                'message_id': message_id,
                'username': username
            }))

    @sync_to_async
    def save_message(self, username, room, message, message_id):
        # Get room object
        try:
            room_obj = ChatRoom.objects.get(title=room)
            user_obj = User.objects.get(username=username)
            k = Chat(user=user_obj, room=room_obj, message=message, message_id=message_id, read_status=False)
            k.save()
        except ChatRoom.DoesNotExist:
            raise Exception("Not a valid chat room.")