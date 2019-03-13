import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View, generic
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q


from Accounts.models import Author
from Accounts.models import Friendship

from .serializers import FollowingSerializers, FollowerSerializers, ExtendAuthorSerializers

from rest_framework.response import Response

# Create your views here.


class AuthorAPI(APIView):
    model = Author

    def get(self, request,*args, **kwargs):
        response = {"query":'author'}
        try:
            current_user = Author.objects.get(id=kwargs['pk'])
            author_data = ExtendAuthorSerializers(current_user).data
            for i in author_data.keys():
                response[i] = author_data[i]

            
            followings = FollowingSerializers(current_user).data['friends']
            followers = FollowerSerializers(current_user).data['follower']
            following_id = []
            for f in followings:
                following_id.append(str(f['author']))
            follower_id = []
            for f in followers:
                follower_id.append(str(f['author']))
            
            friends = list(set(following_id) & set(follower_id))
            
            response['friends'] = []
            for friend in friends:
                friend_data = ExtendAuthorSerializers(Author.objects.get(id=friend)).data 
                response['friends'].append(str(friend_data))
            return Response(response)
        except:
            response['authors'] = []
        return Response(response, status=400)



@csrf_exempt
def unfriend_request(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode())
        if request_body['query'] == "unfriendrequest":
            init_user = Author.objects.get(id=request_body['author']['id'])
            recv_user = Author.objects.get(id=request_body['friend']['id'])
            response = {"query":'unfriendrequest'}
            try:
                Friendship.objects.filter(init_id=init_user, recv_id=recv_user).delete()    # pylint: disable=maybe-no-member
                response['success'] = True
                response['message'] = 'Unfriend request sent'
                return HttpResponse(json.dumps(response), 200)
            except:
                response['success'] = False
                response['message'] = 'Unfriend request sent'
                return HttpResponse(json.dumps(response), status=400)
    return HttpResponse(400)


@csrf_exempt
def friend_request(request):
    if request.method == 'POST':
        request_body = json.loads(request.body.decode())
        if request_body['query'] == 'friendrequest':
            init_user = Author.objects.get(id=request_body['author']['id'])
            recv_user = Author.objects.get(id=request_body['friend']['id'])
            response = {"query":'friendrequest'}
            try:
                
                friendship = Friendship(init_id=init_user, recv_id=recv_user, starting_date=datetime.datetime.now(), status=0)
                friendship.save()
                response['success'] = True
                response['message'] = 'Friend request sent'
                return HttpResponse(json.dumps(response), 200)
            except:
                response['success'] = False
                response['message'] = 'Friend request sent'
                return HttpResponse(json.dumps(response), status=400)
    return HttpResponse(400)


# for api/author/{author_id}/following
class AuthorFollowing(View):
    model=Author
    # get a list of author's following authors
    def get(self, request,*args, **kwargs):
        response = {"query":'friends'}
        try:
            current_user = Author.objects.get(id=kwargs['pk'])
            followings = FollowingSerializers(current_user).data['friends']
            response['authors'] = []
            for friend in followings:
                print(type(friend['author']))
                response['authors'].append(str(friend['author']))
            return HttpResponse(json.dumps(response), 200)
        except:
            response['authors'] = []
        return HttpResponse(json.dumps(response), 400)
    
    def post(self, request,*args, **kwargs):
        request_body = json.loads(request.body.decode())
        request_friends = request_body['authors']
        for friend in request_friends:
            friend = str(friend)
        response = {"query":'friends'}
        try:
            current_user = Author.objects.get(id=kwargs['pk'])
            followings = FollowingSerializers(current_user).data['friends']
            
            
            following_id = []
            for f in followings:
                following_id.append(str(f['author']))
            
            response['authors'] = []
            for friend in following_id:
                if str(friend) in request_friends:
                    response['authors'].append(str(friend))
            return HttpResponse(json.dumps(response), 200)
        except:
            response['authors'] = []
        return HttpResponse(json.dumps(response), 400)

# for api/author/{author_id}/follower/
class AuthorFollower(APIView):
    model=Author
    
    # get a list of author's followers
    def get(self, request,*args, **kwargs):
        response = {"query":'friends'}
        try:
            current_user = Author.objects.get(id=kwargs['pk'])
            followers = FollowerSerializers(current_user).data['follower']
            
            response['authors'] = []
            for friend in followers:
                response['authors'].append(str(friend['author']))
            return Response(response)
        except:
            response['authors'] = []
        return Response(response, status=400)
    

# for api/author/{author_id}/friends
class AuthorFriends(APIView):

    def get(self, request,*args, **kwargs):
        response = {"query":'friends'}
        try:
            current_user = Author.objects.get(id=kwargs['pk'])
            followings = FollowingSerializers(current_user).data['friends']
            followers = FollowerSerializers(current_user).data['follower']
            
            following_id = []
            for f in followings:
                following_id.append(str(f['author']))

            follower_id = []
            for f in followers:
                follower_id.append(str(f['author']))
            
            friends = list(set(following_id) & set(follower_id))
            response['authors'] = friends
            return Response(response)

        except:
            response['authors'] = []
            
        return Response(response, status=400)
    
    # Ask a service if anyone in the list is a friend
    @method_decorator(csrf_exempt)
    def post(self, request,*args, **kwargs):
        request_body = json.loads(request.body.decode())
        request_friends = request_body['authors']
        for friend in request_friends:
            friend = str(friend)
        response = {"query":'friends'}
        try:
            current_user = Author.objects.get(id=kwargs['pk'])
            followings = FollowingSerializers(current_user).data['friends']
            followers = FollowerSerializers(current_user).data['follower']
            
            following_id = []
            for f in followings:
                following_id.append(str(f['author']))

            follower_id = []
            for f in followers:
                follower_id.append(str(f['author']))
            
            friends = list(set(following_id) & set(follower_id))
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
        prefix_url = request.get_host() + "/"
        author_url1, author_url2 = prefix_url + author_id1, prefix_url + author_id2
        
        author1 = Author.objects.filter(id=author_id1)
        author2 = Author.objects.filter(id=author_id2)
        if (author1.exists() and author2.exists()):
            relations = Friendship.objects.filter((Q(init_id=author_id1)&Q(recv_id=author_id2))|    # pylint: disable=maybe-no-member
                                            (Q(init_id=author_id2)&Q(recv_id=author_id1)))          
            areFriends = "True" if (relations.exists() and relations[0].status == 1) else "False"
        else:
            #will be done on next part, at least one of author not exists on this server
            return Response(status=status.HTTP_400_BAD_REQUEST)

        res_body = {"query": "friends",
                    "authors": [author_url1, author_url2],
                    "friends":  areFriends}
        return Response(res_body)

# service/author/posts
class AuthorizedPostsHandler(APIView):
    def get(self, request):
        return Response()


