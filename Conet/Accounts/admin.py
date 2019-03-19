from django.contrib import admin
from django.contrib.auth.models import AbstractUser
from .models import Author, Friendship
# Register your models here.

admin.site.register(Author)
admin.site.register(Friendship)
#admin.site.register(AbstractUser)