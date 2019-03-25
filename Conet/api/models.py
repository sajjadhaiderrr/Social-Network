from django.db import models

# Create your models here.

#This model is used for validation of remote nodes
class Node(models.Model):
    host = models.URLField(primary_key=True, default="")
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)
    sharePosts = models.BooleanField(default=True)
    shareImgs = models.BooleanField(default=True)

#This model is used for accessing endpoints on remote nodes
class RemoteAccount(models.Model):
    host = models.URLField(primary_key=True, default="")
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=100)