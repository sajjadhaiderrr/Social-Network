from Accounts.models import Author
from Accounts.models import Friendship
from django.db import models
from rest_framework import serializers

class ExtendAuthorSerializers(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        many=True, 
        read_only=True,
        slug_field = 'recv_id')
    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github', 'creator')

class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github')

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = ("init_id", "recv_id")