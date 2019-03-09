from Accounts.models import Author
from Accounts.models import Friendship
from django.db import models
from rest_framework import serializers
import json



# Helper serializer for the api/author/{author_id}
class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github')

class FriendshipSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_receiver')

    def get_receiver(self, obj):
        return AuthorSerializers(obj.recv_id).data

    class Meta:
        model = Friendship
        fields = ("author",)

# Serializer for the api/author/{author_id}
class ExtendAuthorSerializers(serializers.ModelSerializer):
    friends = FriendshipSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github','friends')