from rest_framework import serializers
from posting.models import Post, Comment
from Accounts.models import Author

#reference: https://www.django-rest-framework.org/api-guide

#This class is gonna be moved to app Accounts
class AuthorSerializer(serializers.ModelSerializer):
    #author fields
    
    class Meta:
        model = Author
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    #override some fields
    author = AuthorSerializer(read_only=True)
    comment = serializers.SerializerMethodField()
    #Todo:
    #  page
    #  size
    #  count
    #  ...
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('postid')

    def get_comment(self, obj):
            comments = Comment.objects.filter(post=obj.postid)
            serializer = CommentSerializer(comments, many=True)
            return serializer.data

    def create(self, validated_data):
        author = self.context['Author']
        return Post.objects.create(author, **validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        return