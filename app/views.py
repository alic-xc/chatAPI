from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from app.models import Chat, ChatRoom
from app.serializers import UserSerializer, ChatSerializer, ChatRoomSerializer, ChatPatchSerializer


class UserViewSet(ModelViewSet):
    """ Create a user viewset. AllowAny permission during registration only. """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)


class ChatRoomViewSet(ModelViewSet):
    serializer_class = ChatRoomSerializer
    queryset = ChatRoom.objects.all()
    permission_classes = [AllowAny]

    def get_queryset(self):
        return self.queryset.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ChatViewSet(ModelViewSet):
    http_method_names = ['get', 'patch']
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()
    permission_classes = [AllowAny]
    lookup_field = 'message_id'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        else:
            return ChatPatchSerializer

    def get_queryset(self):
        room = self.request.query_params.get('room')
        if room:
            qs = self.queryset.filter(room__title=room)
        else:
            qs = self.queryset.filter(id=self.request.user.id)

        return qs

    def get_object(self):
        return get_object_or_404(Chat, message_id=self.kwargs['message_id'])