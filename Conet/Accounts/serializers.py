from rest_framework import serializers


class AuthorSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    bio = serializers.CharField(required=False, allow_black=True, max_length=200)
    host = serializers.CharField(required=True)
    displayName = serializers.CharField()
    
    # user may provide an invalid github url.
    github = serializers.URLField()
    
    # need to be done
    url = serializers.URLField()
    