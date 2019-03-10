from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from posting.models import Post, Comment
from posting.serializers import PostSerializer
from django.shortcuts import render, get_object_or_404, get_list_or_404, render
from rest_framework.pagination import PageNumberPagination


# Create your views here.

#https://stackoverflow.com/questions/34043378/how-to-paginate-response-from-function-based-view-of-django-rest-framework
class AuthorPostHandler(APIView):
    def get(self, request):
        current_user = request.user
        if (current_user.id):
            postsToGet = get_list_or_404(Post.objects.order_by('published'), author=current_user.id)
            paginator = PageNumberPagination()
            paginator.page_size = 10
            results = paginator.paginate_queryset(postsToGet, request)
            serializer = PostSerializer(results, many=True)
            return paginator.get_paginated_response(serializer.data)
        return

class CreatePostHandler(APIView):
    def post(self, request, format=None):
        current_user = request.user
        if (current_user.id):
            author = current_user.id
            data = request.data
            serializer = PostSerializer(data=data, context={'author': author,})
            if serializer.is_valid():
                serializer.save()
                responseBody = {
                    "query": "createPost",
                    "success": True,
                    "message": "Post has been created"
                }
                return Response(responseBody, status=status.HTTP_200_OK)
            else:
                return Reponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
