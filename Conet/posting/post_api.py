from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from posting.models import Post, Comment
from api.serializers import PostSerializer, CommentSerializer
from django.shortcuts import render
from Accounts.models import Author
from api.ApiHelper import get_friends
import json

### API START

# path: /posts
class ReadAllPublicPosts(APIView):
    # get: All posts marked as public on the server
    def get(self, request):
        posts = Post.objects.filter(visibility="PUBLIC") # pylint: disable=maybe-no-member
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# path: /posts/{post_id}
class ReadSinglePost(APIView):
    # get: Access to a single post with id = `post_id`
    def get(self, request, post_id):
        #first we check to see if the post with the id exists
        post = Post.object.get(pk = post_id).exists()
        if (not post):
            return Response("Post does not exist.", status=200)
        
        #then we check if its unlisted
        if (post.unlisted == True):
            return Response("Post is unlisted", status=200)
        
        #if the posts visibility is set
        #to PUBLIC, we are ok to return it
        if (post.visibility == "PUBLIC"):
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)

        #otherwise, the other privacy settings
        #require that an author be logged in

        #lets check if an author is logged in first
        
        if (not Author.objects.get(id=request.user.id).exists()):
            return Response("Please log in.", status=200)
        
        author = request.user.id
        
        #if the visibility is set to FRIENDS,
        #lets check if the current author is in
        #the posting authors friends list
        author_of_post = post.author
        if (post.visibility == "FRIENDS"):
            friends = get_friends(author_of_post)
            if (author not in friends):
                return Response("You are not a friend of the author.", status=200)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)
        
        #if the visibility is set to FOAF,
        #lets check if the current author is in
        #the posting authors friends of friends list
        if (post.visibility == "FOAF"):
            friends = get_friends(author_of_post)
            friends_of_friends = []
            for friend in friends:
                friends_of_friends += get_friends(friend)
            if (author not in friends_of_friends):
                return Response("You are not a FOAF of the author.", status=200)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)

        #if the visibility to SERVERONLY,
        #we check if the current author is in
        #the posting authors friends list
        #and we check the posting authors
        #host and compare it with the current authors
        if (post.visibility == "SERVERONLY"):
            local_server = author_of_post.host
            friends = get_friends(author_of_post)
            if (author not in friends):
                return Response("You are not a friend of the author.", status=200)
            if (author.host != local_server):
                return Response("You are not on the same server as the author.", status=200)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)
        
        #if the visibility is set to PRIVATE,
        #we check if the current author is in
        #posts visibileTo field
        if (post.visibility == "PRIVATE"):
            if (author not in author_of_post.visibileTo):
                return Response("You are not allowed to see this post.", status=200)
            serializer = PostSerializer(post)
            return Response(serializer.data, status=200)
            
            


    

        if (not Post.objects.filter(pk=post_id).exists()):# pylint: disable=maybe-no-member
            return Response(status=200)
        post = Post.objects.filter(pk=post_id)# pylint: disable=maybe-no-member
        serializer = PostSerializer(post[0])
        return Response(serializer.data)
    # put: update single post with id = post_id
    def put(self, request, post_id):
        if (not Post.objects.filter(pk=post_id).exists()):# pylint: disable=maybe-no-member
            return Response("Invalid Post", status=404)
        else:
            post = Post.objects.get(pk=post_id)# pylint: disable=maybe-no-member
            current_user = Author.objects.get(pk=request.user.id)

            if current_user.id == post.author.id:
                serializer = PostSerializer(post, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response()
                return Response("Invalid data", status=400)

    def delete(self, request, post_id):
        if (not Post.objects.filter(pk=post_id).exists()):# pylint: disable=maybe-no-member
            return Response("Invalid Post", status=404)
        else:
            post = Post.objects.get(pk=post_id)# pylint: disable=maybe-no-member
            current_user = Author.objects.get(pk=request.user.id)

            if current_user.id == post.author.id:
                post.delete()
                return Response()
            return Response("Invalid data", status=400)


# path: /posts/{post_id}/comments
class ReadAndCreateAllCommentsOnSinglePost(APIView):
    # get: Get comments of a post
    def get(self, request, post_id):
        comments = Comment.objects.filter(comment_post=post_id)# pylint: disable=maybe-no-member
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # post: Add a comment to a post
    def post(self, request, post_id):
        curAuthor = Author.objects.get(id=request.user.id)
        post = Post.objects.get(pk=post_id)# pylint: disable=maybe-no-member
        serializer = CommentSerializer(data=request.data, context={'comment_author': curAuthor, 'comment_post': post})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

### API END


### HELPER START

# path /posts/
class PostReqHandler(APIView):
    #handle a request without specifying postid (create new post or get public post)
    # GET: get all posts
    def get(self, request):
        #Todo: get all public posts
        posts = Post.objects.all()# pylint: disable=maybe-no-member
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
        comments = Comment.objects.all()# pylint: disable=maybe-no-member
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
