from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from posting.models import Post, Comment
from posting.serializers import PostSerializer, CommentSerializer
from django.shortcuts import render

# Create your views here.
class PostWithoutIdReqHandler(APIView):
    #handle a request without specifying postid (create new post or get public post)
    def get(self, request):
        #Todo: get all public posts
        return Response()
    def post(self, request):
        curAuthor = None
        #Todo: curAuthor = author who sends request (find out this author)
        serializer = PostSerializer(data=request.data, context={'author': curAuthor,})
        if serializer.is_valid():
            serializer.save()
            #Todo: response success message on json format
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostWithIdReqHandler(APIView):
    #handle a reuqest with a postid
    def get(self, request, postId):  
        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Todo: authentication and decide whether to response the request post or 403
        serializer = PostSerializer(post)
        #Todo: response in json
        return Response(serializer.data)

    def put(self, request, postId):
        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Todo: authentication for modification
        serializer = PostSerializer(post, request.data)
        #Todo: response in json
        if serializer.is_valid():
            serializer.save()
            #Todo: response success message on json format
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, postId):
        try:
            post = Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Todo: authentication for deletion
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommentReqHandler(APIView):
    def get(self, request, postId):
        try:
            Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Comments = Comment.objects.fileter(postid=postId)
        serializer = CommentSerializer(Comments)
        #Todo: change response to json
        return Response(serializer.data)

    def post(self, request, postId):
        try:
            Post.objects.get(pk=postId)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        curAuthor = None
        serializer = PostSerializer(data=request.data, context={'author': curAuthor, 'post': postId})
        if serializer.is_valid():
            serializer.save()
            #Todo: response success message on json format
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)