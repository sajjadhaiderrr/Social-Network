from rest_framework import serializers
from posting.models import Post, Comment
from Accounts.models import Author

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('postid')