import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from Accounts.models import Author
from Accounts.models import Friendship


# Create your views here.

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
