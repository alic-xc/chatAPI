from django.contrib.auth.models import User
from django.db import models


class ChatRoom(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Chat(models.Model):
    room = models.ForeignKey(to=ChatRoom, on_delete=models.CASCADE, related_name='room')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sender')
    message_id = models.CharField(max_length=40)
    message = models.CharField(max_length=1000)
    read_status = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s - %s" % (self.user, self.timestamp)
