from Accounts.models import Author, Friendship, Node 
from .serializers import FollowerSerializers, FollowingSerializers

import requests
from requests.auth import HTTPBasicAuth
import json

def check_friend_of_friend():
    
    return True

def host_cat_authorid(authorObj):
    return authorObj.host + '/author/' + str(authorObj.id)

def get_all_friend_requests(authorObj):
    friendRequests = Friendship.objects.filter(recv_id=authorObj, state=0) # pylint: disable=maybe-no-member
    response = list()
    for request in friendRequests:
        response.append(
            {'id': host_cat_authorid(request.init_id),
            'host': request.init_id.host,
            'displayName': request.init_id.displayName,
            'url': request.init_id.url})
    return response

def get_two_authors_relation(authorObj1, authorObj2):
    #friendship = Friendship.objects.filter(init_id=authorObj1, recv_id=authorObj2)
    #reverse_friendship = Friendship.objects.filter(init_id=authorObj2, recv_id=authorObj1)
    return None


# get a list of friends of given user
def get_friends(user):
    followings = FollowingSerializers(user).data['friends']
            
    # get people who is following current user
    followers = FollowerSerializers(user).data['followers']

    # parse result from serializers. following_id will be a list of strings of UUID
    following_id = []
    follower_id = []

    for f in followings:
        following_id.append(str(f['author']))
    
    for f in followers:
        follower_id.append(str(f['author']))
            
    # find who is both followed by current user and following current user
    friends = list(set(following_id) & set(follower_id))
    return friends

def get_from_remote_server(authorObj, mode=None):
    if mode == 'friends':
        url = '{}/author/{}/friends'.format(authorObj.host, authorObj.id)
    else:
        url = '{}/author/{}'.format(authorObj.host, authorObj.id)

    node = Node.objects.get(foreignHost=authorObj.host) # pylint: disable=maybe-no-member
    res = requests.get(url, auth=HTTPBasicAuth(node.remoteUsername, node.remotePassword))
    return (json.loads(res.text), res.status_code)

def local_author(authorObj, host):
    return True if authorObj.host == ('http://' + host) else False
