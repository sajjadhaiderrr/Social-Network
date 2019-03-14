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
        comments = Comment.objects.filter(post=obj.postid).order_by('published')
        serializer = CommentSerializer(comments, many=True)
        return serializer.data

    # def create(self, validated_data):
    #     #for fields which are no belonged to, might need to pop that data
    #     author = self.context['Author']
    #     post = Post.objects.create(author, **validated_data)
    #     src = 'http://hostname/posts/{}'.format(post.postid)
    #     post.source = post.origin = src
    #     post.save()
    #     return post

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    # def create(self, validated_data):
    #     author = self.context['author']
    #     post = self.context['post']
    #     return Comment.objects.create(author=author, post=post, **validated_data)
