from rest_framework.response import Response
from posting.models import Post, Comment
from django.shortcuts import redirect, render, get_object_or_404

def createPost(request):
    return render(request, "createpost.html")
