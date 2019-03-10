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
        #Todo: check if current user 
        #curAuthor = author who sends request
        #source, origin ?

        curAuthor = None
        serializer = PostSerializer(data=request.data, context={'author': curAuthor,})
        if serializer.is_valid():
            serializer.save()
            #Todo: response success message on json format
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostWithIdReqHandler(APIView):
    #handle a reuqest with a postid
    def get(self, request, postid):  
        try:
            post = Post.objects.get(pk=postid)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        #Todo: check authentication and decide whether to response the request post or 403
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, postid):
        try:
            post = Post.objects.get(pk=postid)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response()

    def delete(self, request, postid):
        try:
            post = Post.objects.get(pk=postid)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response()

class CommentReqHandler(APIView):
    def get(self, request, postid):
        try:
            Post.objects.get(pk=postid)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        Comments = Comment.objects.fileter(postid=postid)
        serializer = CommentSerializer(Comments)
        return Response(serializer.data)

    def post(self, request, postid):
        try:
            Post.objects.get(pk=postid)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response()