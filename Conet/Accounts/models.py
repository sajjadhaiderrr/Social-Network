from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class Author(AbstractUser):
    class Meta(AbstractUser.Meta):
        pass