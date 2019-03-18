from rest_framework import serializers
from posting.models import Post, Comment
from Accounts.models import Author
from api.serializers import AuthorSerializer

#reference: https://www.django-rest-framework.org/api-guide
class PostSerializer(serializers.ModelSerializer):
    #override some fields
    #author = AuthorSerializer(read_only=True)
    #comments = serializers.SerializerMethodField()
    #Todo:
    #  count
    #  size
    #  ...
    class Meta:
        model = Post
        fields = '__all__'

    def get_comment(self, obj):
        comments = Comment.objects.filter(post=obj.postid).order_by('published')    # pylint: disable=maybe-no-member
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    def create(self, validated_data):
        #for fields which are no belonged to, might need to pop that data
        author = self.context['author']
        origin = self.context['origin']
        post = Post.objects.create(author=author, origin=origin, source=origin, **validated_data)  # pylint: disable=maybe-no-member
        src = origin+'/'+str(post.postid)+'/'    # pylint: disable=maybe-no-member
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
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    # def create(self, validated_data):
    #     author = self.context['author']
    #     post = self.context['post']
    #     return Comment.objects.create(author=author, post=post, **validated_data)
