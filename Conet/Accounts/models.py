from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Author(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Meta(AbstractUser.Meta):
        pass

class Friendship(models.Model):
    init_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='creator')
    recv_id = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='assignee')
    starting_date = models.DateTimeField(auto_now=True)