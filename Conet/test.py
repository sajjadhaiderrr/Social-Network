from api import serializers
from Accounts import models

author = models.Author.objects.get(username='test1')
s = serializers.AuthorFriendIDSerializers(author)
s.data