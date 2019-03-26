from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import socket

class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    bio = models.CharField(max_length=200, default="None", null=True)
    host = models.CharField(default="", max_length=50)
    displayName = models.CharField(max_length=30, default="")
    github = models.URLField(default="")
    url = models.URLField(default="", max_length=100)
    
    class Meta(AbstractUser.Meta):
        pass

class Friendship(models.Model):
    init_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='friends')
    recv_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='follower')
    starting_date = models.DateTimeField(auto_now=True)
    # friendship status
    # 0: pending
    # 1: init_id follows recv_id
    state = models.IntegerField(default=0)

    class Meta:
        unique_together = ('init_id', 'recv_id')

#This model is used for validation of remote nodes
class Node(models.Model):
    # used for validation of remote nodes
    foreignHost = models.URLField(primary_key=True, default="")
    authUser = models.OneToOneField(Author, on_delete=models.CASCADE, related_name="node")
    sharePosts = models.BooleanField(default=True)
    shareImgs = models.BooleanField(default=True)
    # use for accessing endpoints on remote nodes
    remoteUsername = models.CharField(max_length=50)
    remotePassword = models.CharField(max_length=200)