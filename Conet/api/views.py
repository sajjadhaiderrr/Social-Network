import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View, generic

from Accounts.models import Author
from Accounts.models import Friendship

from .serializers import FollowingSerializers, FollowerSerializers, ExtendAuthorSerializers

from rest_framework.response import Response

# Create your views here.


class AuthorAPI(View):
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
            return HttpResponse(json.dumps(response), 200)
        except:
            response['authors'] = []
        return HttpResponse(400)



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
        return HttpResponse(400)
    
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
        return HttpResponse(400)


# for api/author/{author_id}/follower/
class AuthorFollower(View):
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
            return HttpResponse(json.dumps(response), 200)
        except:
            response['authors'] = []
        return HttpResponse(400)
    

# for api/author/{author_id}/friends
class AuthorFriends(View):

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
            return HttpResponse(json.dumps(response), 200)

        except:
            response['authors'] = []
            
        return HttpResponse(400)
    
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
            return HttpResponse(json.dumps(response), 200)
        except:
            response['authors'] = []
        return HttpResponse(400)


