from Accounts.models import Author
from Accounts.models import Friendship
from django.db import models
from rest_framework import serializers
import json



# Helper serializer for the api/author/{author_id}
class Helper_AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github')

# Helper serializer for the api/author/{authod_id}
class Helper_AuthorFriendSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_receiver')

    def get_receiver(self, obj):
        return Helper_AuthorSerializers(obj.recv_id).data

    class Meta:
        model = Friendship
        fields = ("author",)

# Serializer for the api/author/{author_id}
class ExtendAuthorSerializers(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github')


class Helper_FollowingSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_receiver')

    def get_receiver(self, obj):
        return obj.recv_id.id

    class Meta:
        model = Friendship
        fields = ("author",)


class FollowingSerializers(serializers.ModelSerializer):
    friends = Helper_FollowingSerializers(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ('friends',)


class Helper_FollowerSerializers(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_receiver')

    def get_receiver(self, obj):
        return obj.init_id.id

    class Meta:
        model = Friendship
        fields = ("author",)

class FollowerSerializers(serializers.ModelSerializer):
    follower = Helper_FollowerSerializers(many=True, read_only=True)
    class Meta:
        model = Friendship
        fields = ('follower',)