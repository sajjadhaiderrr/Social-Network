from Accounts.models import Author, Friendship, Node 
from .serializers import FollowerSerializers, FollowingSerializers

import requests
from requests.auth import HTTPBasicAuth
import json
import socket

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
    # Todo: change id to url format
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
    #friends = update_remote_friends(user, friends, 'http://' + hostname)
    return friends

def update_friends(user, host):
    host = 'http://' + host
    local_friends = list()
    remote_friends = dict()

    follower_frdships = Friendship.objects.filter(recv_id=user) # pylint: disable=maybe-no-member
    following_frdships = Friendship.objects.filter(init_id=user) # pylint: disable=maybe-no-member


    for follower in follower_frdships:
        for following in following_frdships:
            if follower.init_id == following.recv_id:
                if follower.init_id.host == host:
                    local_friends.append(follower.init_id.url)
                else:
                    remote_host = follower.init_id.host
                    remote_friends[remote_host] = remote_friends.get(remote_host, [])
                    remote_friends[remote_host].append(follower.init_id.url)
                break

    new_remote_friends = list()
    for host, friends in remote_friends.items():
        friends_api = host + '/author/' + user.id + '/friends'
        send_query = {'query': 'friends',
                 'authors': friends}

        print('friends_api: ', friends_api)
        
        node = Node.objects.get(foreignHost=host)  # pylint: disable=maybe-no-member
        res = requests.post(friends_api, data=json.dumps(send_query), 
                            auth=HTTPBasicAuth(node.remoteUsername, node.remotePassword))
        friend_query = res.json()
        #Todo: convert urls to ids

        #add = list(set(friend_query['authors']) - set(friends))
        remove_list = list(set(friends) - set(friend_query['authors']))
        new_remote_friends += list(set(friends) & set(friend_query['authors']))
        remove_remote_friends(user, remove_list)

    return local_friends + new_remote_friends

def remove_remote_friends(local_author, remove_list):
    friendship = Friendship.objects.filter(init_id=local_author, recv_id__in=remove_list)  # pylint: disable=maybe-no-member
    reverse_friendship = Friendship.objects.filter(init_id__in=remove_list, recv_id=local_author)  # pylint: disable=maybe-no-member
    friendship.delete()
    reverse_friendship.delete()
    return


def create_remote_author(authorObj):
    username = authorObj['id']
    password = '!@#$%^&*'
    
    try:
        author = Author(username=username, password=password, 
                        id=authorObj['id'], host=authorObj['host'], 
                        displayName=authorObj['displayname'], url=authorObj['url'])
        author.save()
    except:
        return False
    return True

def local_author(authorObj, host):
    return True if authorObj.host == ('http://' + host) else False

def is_local_request(request):
    try:
        request.user.node
    except:
        return True
    return False


'''def get_from_remote_server(authorObj, mode=None):
    if mode == 'friends':
        url = '{}/author/{}/friends'.format(authorObj.host, authorObj.id)
    else:
        url = '{}/author/{}'.format(authorObj.host, authorObj.id)

    node = Node.objects.get(foreignHost=authorObj.host) # pylint: disable=maybe-no-member
    res = requests.get(url, auth=HTTPBasicAuth(node.remoteUsername, node.remotePassword))
    return (json.loads(res.text), res.status_code)'''
