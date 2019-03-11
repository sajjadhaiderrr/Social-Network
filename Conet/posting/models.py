import uuid
from django.db import models
#from django.apps import apps

# Create your models here.

content_type_choice = (
    ('text/plain', 'text/plain'),
    ('text/markdown', 'text/markdown'),
    ('application/base64', 'application/base64'),
    ('image/png;base64', 'image/png;base64'),
    ('image/jpeg;base64 ', 'image/jpeg;base64 '),
)

class Post(models.Model):
    
    visible_type_choice = (
        ('PRIVATE', 'private to visibleTo list'),
        ('FRIENDS', 'private to my friends'),
        ('FOAF', 'private to friends of friends'),
        ('SERVERONLY', 'private to only firends on local server'),
        ('PUBLIC', 'public'),
    )

    postid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=128)
    source = models.URLField(null=True)
    origin = models.URLField(null=True)
    description = models.CharField(max_length=200)
    author = models.ForeignKey('Accounts.Author', on_delete=models.CASCADE)
    contentType = models.CharField(max_length=32, choices=content_type_choice, default='text/plain')
    content = models.TextField(blank=True)
    categories = models.CharField(max_length=250)
    published = models.DateTimeField(auto_now=True)
    visibility = models.CharField(max_length=10, choices=visible_type_choice, default='PUBLIC')
    visibleTo = models.TextField(blank=True)
    unlisted = models.BooleanField(default=False)

class Comment(models.Model):

    commentid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey('Accounts.Author', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    contentType = models.CharField(max_length=32, choices=content_type_choice, default='text/plain')
    published = models.DateTimeField(auto_now_add=True)

