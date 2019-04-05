from Accounts.models import Author
from Accounts.models import Friendship
from posting.models import Post, Comment
from django.db import models
from rest_framework import serializers
import json
from django.db.models import F

#Author serializer for GET, PUT author profile
class AuthorSerializer(serializers.ModelSerializer):
    #author fields
    #author model doesn't need to store url, which gonna be moved to serializer
    url = serializers.SerializerMethodField()
    class Meta:
        model = Author
        #fields = '__all__'
        fields = ('id', 'bio', 'host', 'displayName', 'github', 'url')

    def get_url(self, obj):
        return "{}/author/{}".format(obj.host, obj.id)

# Helper serializer for the api/author/{author_id}
class Helper_AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'email', 'bio', 'host', 'first_name', 'last_name', 'displayName', 'url', 'github')

# Helper serializer for the api/author/{author_id}
class Helper_CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id','author', 'post', 'comment', 'contentType', 'published')

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
    #friends = Helper_FollowingSerializers(many=True, read_only=True)
    friends = serializers.SerializerMethodField()

    def get_friends(self, obj):
        friendships = Friendship.objects.filter(init_id=obj.id) # pylint: disable=maybe-no-member
        friends = Helper_FollowingSerializers(friendships, many=True)
        return friends.data

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
    followers = serializers.SerializerMethodField()

    def get_followers(self, obj):
        friendships = Friendship.objects.filter(recv_id=obj.id) # pylint: disable=maybe-no-member
        followers = Helper_FollowerSerializers(friendships, many=True)
        return followers.data

    class Meta:
        model = Friendship
        fields = ('followers',)


#reference: https://www.django-rest-framework.org/api-guide
class PostSerializer(serializers.ModelSerializer):
    #override some fields
    #author = AuthorSerializer(read_only=True)
    #comments = serializers.SerializerMethodField()
    #Todo:
    #  count
    #  size
    #  ...
    author = serializers.SerializerMethodField('get_author_data')
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.postid

    def get_author_data(self, obj):
        return Helper_AuthorSerializers(Author.objects.get(id=obj.postauthor.id)).data

    comments = serializers.SerializerMethodField('get_comments_list')
    def get_comments_list(self, obj):
        try:
            allcomments = Comment.objects.filter(post=obj.postid).order_by(F("published").desc())
            serializer = CommentSerializer(allcomments, many=True)
            return serializer.data
        except Exception as e:
            return e

    class Meta:
        model = Post
        fields = ('author', 'title', 'source', 'origin', 'description', 'contentType', 'published', 'content','visibility','visibleTo','unlisted','comments')

    

    def create(self, validated_data):
        #for fields which are no belonged to, might need to pop that data
        author = self.context['author']
        origin = self.context['origin']
        post = Post.objects.create(postauthor=author, origin=origin, source=origin, **validated_data)  # pylint: disable=maybe-no-member
        src = origin+'posts/'+str(post.postid)   # pylint: disable=maybe-no-member
        post.source = post.origin = src
        post.save()
        return post

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.contentType = validated_data.get('contentType', instance.contentType)
        instance.visibility = validated_data.get('visibility', instance.visibility)
        instance.origin = validated_data.get('origin', instance.origin)
        instance.source = validated_data.get('source', instance.source)
        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    def get_commentauthor(self, obj):
        return Helper_AuthorSerializers(Author.objects.get(id=obj.commentauthor.id)).data

    author = serializers.SerializerMethodField('get_commentauthor')
    class Meta:
        model = Comment
        fields = ('id','post','author', 'comment', 'contentType', 'published')

    
    def create(self, validated_data):
        print(validated_data)
        data = {}
        data['post'] = validated_data['post']
        data['commentauthor'] = self.context['author']
        data['comment'] = validated_data['comment']
        data['contentType'] = validated_data['contentType']
        comment = Comment.objects.create(**data)  # pylint: disable=maybe-no-member
        comment.save()
        return comment

