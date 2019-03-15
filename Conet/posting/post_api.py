from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from posting.models import Post, Comment
from posting.serializers import PostSerializer, CommentSerializer
from django.shortcuts import render
from Accounts.models import Author
import json

### API START

# path: /posts
class ReadAllPublicPosts(APIView):
    # get: All posts marked as public on the server
    def get(self, request):
        posts = Post.objects.filter(visibility="PUBLIC")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# path: /posts/{post_id}
class ReadSinglePost(APIView):
    # get: Access to a single post with id = `post_id`
    def get(self, request, post_id):
        post = Post.objects.filter(pk=post_id)
        serializer = PostSerializer(post[0])
        return Response(serializer.data)
    # put: update single post with id = post_id
    def put(self, request, post_id):
        if (not Post.objects.filter(pk=post_id).exists()):
            return Response("Invalid Post", satus=404)
        else:
            post = Post.objects.get(pk=post_id)
            current_user = Author.objects.get(pk=request.user.id)

            if current_user == post.author.id:
                serializer = PostSerializer(data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response()
                return Response("Invalid data", serializer.errors, status=400)


# path: /posts/{post_id}/comments
class ReadAndCreateAllCommentsOnSinglePost(APIView):
    # get: Get comments of a post
    def get(self, request, post_id):
        comments = Comment.objects.filter(post=post_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # post: Add a comment to a post
    def post(self, request, post_id):
        request.data["post"] = post_id
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### API END


### HELPER START

# path /posts/
class PostReqHandler(APIView):
    #handle a request without specifying postid (create new post or get public post)
    # GET: get all posts
    def get(self, request):
        #Todo: get all public posts
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        # POST: Create a post
        curAuthor = Author.objects.get(id=request.user.id)
        origin = request.scheme+ "://" +request.get_host()+ "/"
        serializer = PostSerializer(data=request.data, context={'author': curAuthor, 'origin': origin})
        if serializer.is_valid():
            serializer.save()
            #Todo: response success message on json format
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentReqHandler(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #Todo: response success message on json format
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### HELPER END
