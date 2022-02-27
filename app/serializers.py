from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from app.models import Chat, ChatRoom


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        email = data['email']
        username = data['username']

        try:
            user = User.objects.filter(Q(email=email) | Q(username=username))
            if len(user) > 0:
                raise serializers.ValidationError('Email/Username already exist. Please choose another and try again')

        except User.DoesNotExist:
            pass

        return data

    def create(self, validated_data):
        """
        * Create new user,
        * Hash user password,
        """
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return validated_data


class ChatSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Chat
        fields = '__all__'
        depth=1


class ChatPatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'message_id', 'read_status']


class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        # fields = '__all__'
        exclude = ['user']