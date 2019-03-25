import datetime
import json
from django.db.models import F
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View, generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import JsonResponse


from Accounts.models import Author
from Accounts.models import Friendship
from posting.models import Post

from .serializers import FollowingSerializers, FollowerSerializers, ExtendAuthorSerializers, AuthorSerializer, Helper_AuthorSerializers, PostSerializer
from . import ApiHelper

# Create your views here.

# api for /author
class AuthorAPI(APIView):
    model = Author
    def get(self, request,*args, **kwargs):
        response = {"query":'author'}
        try:
            # get current user
            current_user = Author.objects.get(id=kwargs['pk'])
            # get current user's data. Note that friends' data is excluded
            author_data = ExtendAuthorSerializers(current_user).data
            
            # append each data to response
            for i in author_data.keys():
                response[i] = author_data[i]
            friends = ApiHelper.get_friends(current_user)
            # append friend's detailed information to response
            response['friends'] = []
            for friend in friends:
                friend_data = Helper_AuthorSerializers(Author.objects.get(id=friend)).data 
                response['friends'].append(json.dumps(friend_data))
            return Response(response, status=200)
        except:
            response['authors'] = []
            return Response(response, status=400)


# /unfriendrequest
# getting POST request from client. Un-friend given initiator and receiver.
class UnfriendRequestHandler(APIView):
    def post(self, request):
        # parse request body
        request_body = request.data
        response = {"query":'unfriendrequest'}
        # instanciate initiator and receiver as Author object
        send_id = request_body['author']['id'].replace(request_body['author']['host']+'/author/','')
        rcv_id = request_body['friend']['id'].replace(request_body['friend']['host']+'/author/','')
        try:
            init_user = Author.objects.get(id=send_id)
            recv_user = Author.objects.get(id=rcv_id)
        except:
            response['message'] = 'Request author or request friend does not exist.'
            return HttpResponse(json.dumps(response), status=400)

        # try to delete the relationship with given init_user and recv_user
        reverse_friendship = Friendship.objects.filter(init_id=recv_user, recv_id=init_user) # pylint: disable=maybe-no-member
        friendship = Friendship.objects.filter(init_id=init_user, recv_id=recv_user) # pylint: disable=maybe-no-member
        print("reverse: ", reverse_friendship)
        if (friendship.exists() or reverse_friendship.exists()):
            #case: there's reverse relationship between two users and there's a pending friend
            #request from recv_user to init_user
            if reverse_friendship.exists() and reverse_friendship[0].state == 0:
                reverse_friendship.update(state=1, starting_date = datetime.datetime.now())
            if friendship.exists():
                friendship.delete()
            
            response['success'] = True
            response['message'] = 'Unfriend request proceeded successfully.'
            return HttpResponse(json.dumps(response), 200)
        else:
            response['success'] = False
            response['message'] = 'Unfriend request failed because request or relationship does not exist.'
            return HttpResponse(json.dumps(response), status=400)

# /friendrequest
class FriendRequestHandler(APIView):
    def get(self, request):
        reqUsrId = request.user.id
        try:
            reqAuthor = Author.objects.get(pk=reqUsrId)
            print("pass here")
            requestList = ApiHelper.get_all_friend_requests(reqAuthor)
            response = {'query': 'friendrequest',
                        'friends': requestList}
            return Response(response)
        except:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        # parse request body
        request_body = request.data
        # response body
        response = {"query":'friendrequest'}

        # instanciate initiator and receiver as Author object
        send_id = request_body['author']['id'].replace(request_body['author']['host']+'/author/','')
        rcv_id = request_body['friend']['id'].replace(request_body['friend']['host']+'/author/','')

        print("send_id: ", send_id)
        print("rcv_id: ", rcv_id)
        try:
            init_user = Author.objects.get(id=send_id)
            recv_user = Author.objects.get(id=rcv_id)
        except:
            response['message'] = 'Request author or request friend does not exist.'
            print("eror here1")
            return HttpResponse(json.dumps(response), status=400)

        # try to get the current relationship between two authors
        try:
            friendship = Friendship.objects.get(init_id=init_user, recv_id=recv_user)   # pylint: disable=maybe-no-member
        except:  
            reverse_friendship = Friendship.objects.filter(init_id=recv_user, recv_id=init_user) # pylint: disable=maybe-no-member
            friendship = Friendship(init_id=init_user, recv_id=recv_user, starting_date=datetime.datetime.now())
            print("reverse: ", reverse_friendship)
            #If there's a reverse relation between init_user and recv_user, they become friend
            #case1: init_user accepts friend request from recv_user
            #case2: both init_user and recv_user send friend request to each other
            #case3: recv_user is following init_user
            if reverse_friendship.exists():
                reverse_friendship.update(state=1, starting_date = datetime.datetime.now())
                friendship.state = 1
                friendship.save()
                response['message'] = 'Your friend request is accepted.'
            #init_user sends a friend request to recv_user and there's no reverse relationship
            else:
                friendship.state = 0
                friendship.save()
                response['message'] = 'Your friend request is sent successfully.'
            response['success'] = True
            return HttpResponse(json.dumps(response), 200)
            #friend request is sent already or init_user is already followed to recv_user
        if friendship.state == 0:
            response['message'] = 'You are already sent a friend request to this user.'
        else:
            response['message'] = 'You are already followed this user.'
        return HttpResponse(json.dumps(response), status=400)

#/notification
def notification(request):
    if request.method == 'GET':
        reqUsrId = request.user.id

        try:
            reqAuthor = Author.objects.get(pk=reqUsrId)
            requestList = ApiHelper.get_all_friend_requests(reqAuthor)
            
            author = {'id': ApiHelper.host_cat_authorid(reqAuthor),
                    'host': reqAuthor.host,
                    'displayName': reqAuthor.displayName,
                    'url': reqAuthor.url}

            response = {'query': 'friendrequest',
                        'author': author, 
                        'friends': requestList}

            return render(request,'Accounts/notifications.html', response)
        except:
            return HttpResponse(status=403)
    else:
        return HttpResponseNotAllowed(['GET'])


# for author/{author_id}/following
# getting who is following current user
class AuthorFollowing(View):
    model=Author
    # get a list of author's following authors
    def get(self, request,*args, **kwargs):
        response = {"query":'friends'}
        try:
            # get current user based on URL on browser. It is the id of user who is currently being viewed.
            current_user = Author.objects.get(id=kwargs['pk'])

            # get people whom this user is following.
            followings = FollowingSerializers(current_user).data['friends']
            response['authors'] = []

            # append each friend's id to a list. For response
            for friend in followings:
                friend_data = Helper_AuthorSerializers(Author.objects.get(id=friend['author'])).data 
                response['authors'].append(friend_data)
            return HttpResponse(json.dumps(response), 200)
        except:
            response['authors'] = []
            return HttpResponse(json.dumps(response), 400)


# for author/{author_id}/follower
class AuthorFollower(APIView):
    model=Author
    
    # get a list of author's followers
    def get(self, request,*args, **kwargs):
        response = {"query":'friends'}
        try:
            # get current user based on URL on browser. It is the id of user who is currently being viewed.
            
            current_user = Author.objects.get(id=kwargs['pk'])
            
            # get people who is following the user shows on screen.
            followers = FollowerSerializers(current_user).data['followers']
            
            response['authors'] = []
            for friend in followers:
                friend_data = Helper_AuthorSerializers(Author.objects.get(id=friend['author'])).data 
                response['authors'].append(friend_data)
            return Response(response)
        except:
            response['authors'] = []
            return Response(response, status=400)
    

# for api/author/{author_id}/friends
class AuthorFriends(APIView):
    # get a list of ids who is friend of given user.
    def get(self, request,*args, **kwargs):
        response = {"query":'friends'}
        try:
            # get current user on URL
            current_user = Author.objects.get(id=kwargs['pk'])

            friends = ApiHelper.get_friends(current_user)
            response['authors'] = friends
            return Response(response)
        except:
            response['authors'] = []
            return Response(response, status=400)
    
    # Ask a service if anyone in the list is a friend
    def post(self, request,*args, **kwargs):
        # parse request body
        request_body = json.loads(request.body.decode())

        # get the authors who are checked be a friend of author shows in URL
        request_friends = request_body['authors']
        for friend in request_friends:
            friend = str(friend)
        response = {"query":'friends'}
        try:
            # get current user on URL
            current_user = Author.objects.get(id=kwargs['pk'])
            
            friends = ApiHelper.get_friends(current_user)
            response['authors'] = []
            for friend in friends:
                if str(friend) in request_friends:
                    response['authors'].append(str(friend))
            return Response(response)
        except:
            response['authors'] = []
        return Response(response, status=400)

#reference: https://docs.djangoproject.com/en/2.1/ref/request-response/

# service/author/<authorid>/friends/<authorid>
class TwoAuthorsRelation(APIView):
    def get(self, request, author_id1, author_id2):
        response = {}
        response['query'] = 'friends'
        try:
            author1 = Author.objects.get(id=author_id1)
            author2 = Author.objects.get(id=author_id2)
            friends = ApiHelper.get_friends(author1)
            
            response['friends'] = author_id2 in friends
            response['authors'] = [author1.url, author2.url]
            return Response(response, status=200)
        except:
            response['friends'] = False
            response['authors'] = ["",""]
            return Response(response, status=400)

# service/author/posts
class AuthorPostsAPI(APIView):
    def get(self, request):
        allposts = []
        page_size = 10
        posts = Post.objects.none() # pylint: disable=maybe-no-member

        #get the posts of all your friends whos visibility is set to FRIENDS
        current_user = Author.objects.get(pk=request.user.id)
        friends = ApiHelper.get_friends(current_user)

        posts = Post.objects.filter(author=request.user)  # pylint: disable=maybe-no-member

        for friend in friends:
            friend = Author.objects.get(pk=friend)       
            newposts = Post.objects.filter(author = friend, visibility = "FRIENDS") # pylint: disable=maybe-no-member
            posts |= newposts

        #get all public posts
        public = Post.objects.filter(visibility="PUBLIC")   # pylint: disable=maybe-no-member
        posts |= public
        posts = posts.order_by(F("published").desc())

        #get posts that satisfy FOAF
        allfoafs = set()
        for friend in friends:
            #direct friend with posts "FOAF" should visible to current user
            friend = Author.objects.get(pk=friend)
            #newposts = Post.objects.filter(visibility="FOAF", author=friend) # pylint: disable=maybe-no-member
            #posts |= newposts
            allfoafs.add(friend)
            foafs = ApiHelper.get_friends(friend)
            for each in foafs:
                allfoafs.add(each)
        
        for foaf in allfoafs:
            newposts = Post.objects.filter(visibility="FOAF", author=foaf) # pylint: disable=maybe-no-member
            posts |= newposts
        
        for post in posts:
            allposts.append(post)
        #foaf end

        #private
        '''
        for friend in friends:
            posts = Post.objcets.filter(author=friend, visibility="PRIVATE") # pylint: disable=maybe-no-member
            for post in posts:
                post.visibleTo'''
        #there are some repeat operations above, might combine later    

        try:
            page = int(request.GET.get("page", 0))
            if (page < 0):
                raise Exception()
            if ((page+1)*page_size >= len(allposts)):
                last_page = True
            else:
                last_page = False
            response_posts = allposts[page * page_size : min((page+1)*page_size, len(allposts))]
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        response = {}
        response['query'] = "posts"
        response['count'] = len(allposts)
        response['size'] = len(response_posts)
        if(page>0):
            response['previous'] = current_user.host + "/author/posts?page="+str(page-1)
        else:
            response['previous'] = "None"

        if(not last_page):
            response['next'] = current_user.host + "/author/posts?page="+str(page+1)
        else:
            response['next'] = "None"

        response['posts'] = []
        for post in response_posts:
            serializer = PostSerializer(post).data
            serializer['postid'] = str(serializer['postid'])
            response['posts'].append(serializer)
        
        return Response(response)

#reference: https://stackoverflow.com/questions/12615154/how-to-get-the-currently-logged-in-users-user-id-in-django

#user profile handler
class AuthorProfileHandler(APIView):
    def get(self, request, authorid):
        try:
            author = Author.objects.get(pk=authorid)
            serializer = AuthorSerializer(author)
            return JsonResponse(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, authorid):
        try:
            reqed_author = Author.objects.get(pk=authorid)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if request.user.id != authorid:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        serializer = AuthorSerializer(reqed_author, data=request.data)
        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

# get a list of ALL(including public, private, FOAF, friend, etc) posts made by given author. 
class AuthorMadePostAPI(APIView):
    def get(self,request,pk):
        try:
            response = {}
            response['query'] = "madeposts"
            author = Author.objects.get(pk=pk)
            posts = Post.objects.filter(author = author).order_by(F("published").desc())   # pylint: disable=maybe-no-member
            serializer = PostSerializer(posts, many=True)
            response['posts'] = serializer.data
            return Response(response, status=status.HTTP_200_OK) 
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
