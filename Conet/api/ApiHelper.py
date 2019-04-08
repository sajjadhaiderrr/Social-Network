from Accounts.models import Author, Friendship, Node 
from .serializers import FollowerSerializers, FollowingSerializers, PostSerializer
import requests
from requests.auth import HTTPBasicAuth
import json
import socket
import uuid
import datetime
import re

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

def obtain_from_remote_node(url, host, method='GET', send_query=None, header={}):
    node = Node.objects.get(foreignHost=host)  # pylint: disable=maybe-no-member
    authentication = HTTPBasicAuth(node.remoteUsername, node.remotePassword)
    try:
        if method == 'GET':
            res = requests.get(url, auth=authentication, headers=header)
        elif method == 'POST':
            header['Content-Type'] = 'application/json'
            res = requests.post(url, headers=header, data=send_query, auth=authentication)
        else:
            return {'code': 405}
        #print("response json: ", res.json())
        return (res.json(), res.status_code)
    except Exception as e:
        print("Exception on remote request: ", e)
        return (None, 500)

def urls_to_ids(url_list):
    pattern = re.compile('.+/author/')
    return [pattern.sub('', url) for url in url_list]

# get a list of friends of given user on local database
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

# get a friend by updating local friendship database if needed
def update_friends(user, host):
    localhost = host if re.match('http://', host) else 'http://' + host
    local_friends = list()
    remote_friends = dict()

    follower_frdships = Friendship.objects.filter(recv_id=user) # pylint: disable=maybe-no-member
    following_frdships = Friendship.objects.filter(init_id=user) # pylint: disable=maybe-no-member


    for follower in follower_frdships:
        for following in following_frdships:
            if follower.init_id == following.recv_id:
                if follower.init_id.host == localhost:
                    local_friends.append(str(follower.init_id.id))
                else:
                    remote_host = follower.init_id.host
                    remote_friends[remote_host] = remote_friends.get(remote_host, [])
                    remote_friends[remote_host].append(follower.init_id.url)
                break

    new_remote_friends = list()
    for host, friends in remote_friends.items():
        friends_api = host + '/author/' + str(user.id) + '/friends'
        send_query = {'query': 'friends',
                    'author': localhost + '/author/' + str(user.id),
                    'authors': friends}

        #print("update friend req: ", send_query)
        friend_query, _ = obtain_from_remote_node(url=friends_api, host=host, 
            method='POST', send_query=json.dumps(send_query))
        #print("update friend res: ", friend_query)
        #add = list(set(friend_query['authors']) - set(friends))
        friends = {friend.replace(host+'/author/', '') for friend in friends}
        friend_query['authors'] = {friend.replace(host+'/author/', '') for friend in friend_query['authors']}
        remove_list = list(friends - friend_query['authors'])
        new_remote_friends += list(friends & friend_query['authors'])
        remove_remote_friends(user, remove_list)
    
    return (local_friends, new_remote_friends)

def remove_remote_friends(local_author, remove_list):
    remote_authors = Author.objects.filter(id__in=remove_list)
    friendship = Friendship.objects.filter(init_id=local_author, recv_id__in=list(remote_authors))  # pylint: disable=maybe-no-member
    reverse_friendship = Friendship.objects.filter(init_id__in=list(remote_authors), recv_id=local_author)  # pylint: disable=maybe-no-member
    friendship.delete()
    reverse_friendship.delete()

def create_remote_author(authorObj):
    authorObj['host'] = authorObj['host'].rstrip('/')
    authorObj['id'] = authorObj['id'].replace(authorObj['host']+'/author/', '')
    username = authorObj['id']
    password = '!@#$%^&*'

    try:
        Author.objects.create_user(username=username, password=password)
        author = Author.objects.filter(username=username)
        author.update(id=authorObj['id'], displayName=authorObj['displayName'],
            host=authorObj['host'], url=authorObj['url'])
    except:
        return (False, None)
    return (True, author[0])

def update_remote_author(request_author, localcpy_author):
    if not request_author['displayName'] == localcpy_author[0].displayName:
        localcpy_author.update(displayName=request_author['displayName'])
    
    return localcpy_author[0]

def format_author_posts(post_list):
    res_query = {"query": "posts",
                 "count": len(post_list),
                 "size": len(post_list),
                 "posts": []}
    
    for post in post_list: 
        post = PostSerializer(post).data
        post['id'] = str(post['id'])
        res_query['posts'].append(post)
    
    return res_query

def local_author(author_host, localhost):
    return True if author_host == ('http://' + localhost) else False

def is_local_request(request):
    try:
        request.user.node
        print(request.user.node)
    except:
        return True
    return False

def is_sharePosts(is_local, userObj):
    if not is_local and not userObj.node.sharePosts:
        return False
    return True

def is_shareImgs(is_local, userObj):
    if not is_local and not userObj.node.shareImgs:
        return False
    return True

def get_request_author(is_local, request):
    if is_local:
        return Author.objects.get(id=request.user.id)
    else:
        request_user_id = request.META.get('HTTP_X_REQUEST_USER_ID', '')
        request_user_id = urls_to_ids([request_user_id])[0]
        return Author.objects.get(id=request_user_id)  

def permission_on_foaf(req_author, rcv_author, is_local):
    #rcv_localfrds, rcv_remotefrds = update_friends(rcv_author, rcv_author.host)
    return False