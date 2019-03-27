from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from posting.models import Post, Comment
from api.serializers import PostSerializer, CommentSerializer
from django.shortcuts import render
from Accounts.models import Author
from api.ApiHelper import get_friends
from django.core.paginator import Paginator

import uuid
import json
import datetime

def CheckPermissions(author, post):
    #if the visibility is set to FRIENDS,
    #lets check if the current author is in
    #the posting authors friends list
    '''
    if (post.visibility == 'PUBLIC'):
        return ("This is a public post.", True)

    if (post.author.id == author.id):
        return ("This is your post", True)
    '''
    author_of_post = post.author
    if (post.visibility == "FRIENDS"):
        friends = get_friends(author_of_post)
        if (str(author.id) not in friends):
            return ("You are NOT a friend of the author.", False)
        return ("You are a friend of the author.", True)
    
    #if the visibility is set to FOAF,
    #lets check if the current author is in
    #the posting authors friends of friends list
    if (post.visibility == "FOAF"):
        friends = get_friends(author_of_post)
        friends_of_friends = []
        for friend in friends:
            friends_of_friends += get_friends(Author.objects.get(pk=friend))
        friends_of_friends += friends
        if (str(author.id) not in friends_of_friends):
            return ("You are NOT a FOAF of the author.", False)
        return ("You are a FOAF of the author.", True)

    #if the visibility to SERVERONLY,
    #we check if the current author is in
    #the posting authors friends list
    #and we check the posting authors
    #host and compare it with the current authors
    if (post.visibility == "SERVERONLY"):
        local_server = author_of_post.host
        friends = get_friends(author_of_post)
        if (author.id not in friends):
            return ("You are NOT a friend of the author.", False)
        if (author.host != local_server):
            return ("You are NOT on the same server as the author.", False)
        return ("You are a friend of and on the same server as the author.", True)

    #if the visibility is set to PRIVATE,
    #we check if the current author is in
    #the posts visibileTo field
    if (post.visibility == "PRIVATE"):
        if (str(author.id) not in post.visibleTo):
            return ("You are NOT one of the people this post is visible to.", False)
        return ("You are one of the people this post is visible to.", True)


### API START

# path: /posts
class ReadAllPublicPosts(APIView):
    # get: All posts marked as public on the server
    def get(self, request):
        response_object = {
            "query":"getPosts",
            "count": None,
            "size": None,
            "next": None,
            "previous": None,
            "comments": None
        }

        request_url = request.build_absolute_uri("/").strip("/")
        previous_page = None

        #start off by  getting the 
        #page and size from the query string
        try:
            page = int(request.GET.get("page", ""))
        except:
            page = ""
        try:
            size = int(request.GET.get("size", ""))
        except:
            size = ""

        posts = Post.objects.filter(visibility="PUBLIC", unlisted = False)  # pylint: disable=maybe-no-member
        count = posts.count()
    
        if (page and size):           
            paginator = Paginator(posts, size)

            if (page > paginator.num_pages):
                posts = None
            else:
                posts = paginator.get_page(page)
            
            response_object["size"] = size
            if (page > 1):
                previous_page = request_url + "/posts?page={}&size={}".format(page-1, size)
            next_page = request_url + "/posts?page={}&size={}".format(page+1, size)
            response_object["next"] = next_page
            response_object["previous"] = previous_page

        serializer = PostSerializer(posts, many=True)
        response_object["comments"] = serializer.data
        response_object["count"] = count
        return Response(response_object, status=status.HTTP_200_OK)

# path: /posts/{post_id}
class ReadSinglePost(APIView):
    # get: Access to a single post with id = `post_id`
    def get(self, request, post_id):
        response_object = {
            "query":"getPost",
            "post": None
        }
        #first we check to see if the post with the id exists
        try:
            post = Post.objects.get(pk=post_id) # pylint: disable=maybe-no-member
            
        except:
            return Response(response_object, status=status.HTTP_200_OK)
        
        #if the posts visibility is set
        #to PUBLIC, we are ok to return it
        if (post.visibility == "PUBLIC"):
            serializer = PostSerializer(post)
            response_object["post"] = serializer.data
            return Response(response_object, status=status.HTTP_200_OK)
        
        #otherwise, the other privacy settings
        #require that an author be logged in

        # lets check if an author is logged in first    
        # here, author has to login in order to view the posts,
        try:
            author = Author.objects.get(id=request.user.id)
        except:
            return Response(response_object, status=status.HTTP_403_FORBIDDEN)
        
        #check if its the currently authenticated
        #users post
        if (author.id == post.author.id):
            serializer = PostSerializer(post)
            response_object["post"] = serializer.data
            return Response(response_object, status=status.HTTP_200_OK)
        
        check_permissions = CheckPermissions(author, post)

        # if current author has no permission:
        if (not check_permissions[1]):
            return Response(response_object, status=status.HTTP_403_FORBIDDEN)
        
        # current user has permission
        serializer = PostSerializer(post)
        response_object["post"] = serializer.data
        return Response(response_object, status=status.HTTP_200_OK)
    

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
        if (not Post.objects.filter(pk=post_id).exists()):  # pylint: disable=maybe-no-member
            return Response("Invalid Post", status=404)
        else:
            post = Post.objects.get(pk=post_id) # pylint: disable=maybe-no-member
            current_user = Author.objects.get(pk=request.user.id)

            if current_user.id == post.author.id:
                post.delete()
                return Response()
            return Response("Invalid data", status=400)


# path: /posts/{post_id}/comments
class ReadAndCreateAllCommentsOnSinglePost(APIView):
    # get: Get comments of a post
    def get(self, request, post_id):

        response_object = {
            "query":"getComments",
            "count": None,
            "size": None,
            "next": None,
            "previous": None,
            "comments": None
        }

        request_url = request.build_absolute_uri("/").strip("/")
        previous_page = None

        #first we check to see if the post with the id exists
        try:
            post = Post.objects.get(pk=post_id) # pylint: disable=maybe-no-member
        except:
            return Response(response_object, status=status.HTTP_200_OK)

        #start off by  getting the 
        #page and size from the query string
        try:
            page = int(request.GET.get("page", ""))
        except:
            page = ""
        try:
            size = int(request.GET.get("size", ""))
        except:
            size = ""
        
        #if the posts visibility is set
        #to PUBLIC, we can return comments
        if (post.visibility == "PUBLIC"):
            comments = Comment.objects.filter(post=post_id) # pylint: disable=maybe-no-member
            count = comments.count()
        
            if (page and size):           
                paginator = Paginator(comments, size)

                if (page > paginator.num_pages):
                    comments = None
                else:
                    comments = paginator.get_page(page)
                
                response_object["size"] = size
                if (page > 1):
                    previous_page = request_url + "/posts/{}/comments?page={}&size={}".format(post_id, page-1, size)
                next_page = request_url + "/posts/{}/comments?page={}&size={}".format(post_id, page+1, size)
                response_object["next"] = next_page
                response_object["previous"] = previous_page

            serializer = CommentSerializer(comments, many=True)
            response_object["comments"] = serializer.data
            response_object["count"] = count
            return Response(response_object, status=status.HTTP_200_OK)

        #otherwise, the other privacy settings
        #require that an author be logged in

        #lets check if an author is logged in first
        try:
            author = Author.objects.get(id=request.user.id)
        except:
            return Response(response_object, status=status.HTTP_200_OK)

        #check if its the currently authenticated
        #users post
        if (author.id == post.author.id):
            comments = Comment.objects.filter(post=post_id) # pylint: disable=maybe-no-member
            count = comments.count()
        
            if (page and size):           
                paginator = Paginator(comments, size)

                if (page > paginator.num_pages):
                    comments = None
                else:
                    comments = paginator.get_page(page)
                
                response_object["size"] = size
                if (page > 1):
                    previous_page = request_url + "/posts/{}/comments?page={}&size={}".format(post_id, page-1, size)
                next_page = request_url + "/posts/{}/comments?page={}&size={}".format(post_id, page+1, size)
                response_object["next"] = next_page
                response_object["previous"] = previous_page

            serializer = CommentSerializer(comments, many=True)
            response_object["comments"] = serializer.data
            response_object["count"] = count
            return Response(response_object, status=status.HTTP_200_OK)
        
        check_permissions = CheckPermissions(author, post)
        if (not check_permissions[1]):
            return Response(response_object, status=status.HTTP_200_OK)
        
        comments = Comment.objects.filter(post=post_id) # pylint: disable=maybe-no-member
        count = comments.count()
        
        if (page and size):
            paginator = Paginator(comments, size)

            if (page > paginator.num_pages):
                comments = None
            else:
                comments = paginator.get_page(page)
            
            response_object["size"] = size
            if (page > 1):
                previous_page = request_url + "/posts/{}/comments?page={}&size={}".format(post_id, page-1, size)
            next_page = request_url + "/posts/{}/comments?page={}&size={}".format(post_id, page+1, size)
            response_object["next"] = next_page
            response_object["previous"] = previous_page

        serializer = CommentSerializer(comments, many=True)
        response_object["comments"] = serializer.data
        response_object["count"] = count
        return Response(response_object, status=status.HTTP_200_OK)

    # post: Add a comment to a post
    def post(self, request, post_id):
        response_object = {
            "query":"addComment",
            "type": None,
            "message": None,
        }
        # initializing data
        data = request.data
        data['author'] = request.user.id
        data['post'] = post_id

        #first we check to see if the post with the id exists
        try:
            post = Post.objects.get(pk=post_id) # pylint: disable=maybe-no-member
        except:
            response_object["type"] = False
            response_object["message"] = "Post does not exist."
            return Response(response_object, status=status.HTTP_404_NOT_FOUND)

        #lets check if an author is logged in first
        try:
            author = Author.objects.get(id=request.user.id)
        except:
            response_object["type"] = False
            response_object["message"] = "Log in to add a comment."
            return Response(response_object, status=status.HTTP_403_FORBIDDEN)
        
        # need to check this part. 'Friend' visibility cannot work?
        if (post.visibility == "PUBLIC"):
            print(data)
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_object["type"] = True
                response_object["message"] = "Successfully added comment."
                return Response(response_object, status=status.HTTP_200_OK)
            response_object["type"] = False
            response_object["message"] = "Could not add comment."
            return Response(response_object, status=status.HTTP_400_BAD_REQUEST)

        #check if its the currently authenticated
        #users post
        if (author.id == post.author.id):
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                response_object["type"] = True
                response_object["message"] = "Successfully added comment."
                return Response(response_object, status=status.HTTP_200_OK)
            response_object["type"] = False
            response_object["message"] = "Could not add comment."
            return Response(response_object, status=status.HTTP_403_FORBIDDEN)
        
        check_permissions = CheckPermissions(author, post)
        if (not check_permissions[1]):
            response_object["type"] = False
            response_object["message"] = "You do not have permissions to add a comment to this post."
            return Response(response_object, status=status.HTTP_403_FORBIDDEN)

        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

            response_object["type"] = True
            response_object["message"] = "Successfully added comment."
            return Response(response_object, status=status.HTTP_200_OK)
        response_object["type"] = False
        response_object["message"] = "Could not add comment."
        return Response(response_object, status=status.HTTP_400_BAD_REQUEST)


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


    def post(self, request, post_id):
        curAuthor = Author.objects.get(id=request.user.id)
        post = Post.objects.get(pk=post_id)# pylint: disable=maybe-no-member

        data = request.data
        data['author'] = curAuthor.id
        data['post'] = post.postid
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            #Todo: response success message on json format
            return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

### HELPER END
