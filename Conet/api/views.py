import datetime
import json
from django.db.models import F
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View, generic

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q
from django.http import JsonResponse


from Accounts.models import Author, Node
from Accounts.models import Friendship
from posting.models import Post

from .serializers import FollowingSerializers, FollowerSerializers, ExtendAuthorSerializers, AuthorSerializer, Helper_AuthorSerializers, PostSerializer
from . import ApiHelper

import requests




def getGitHubPosts(author_id):
        try:
            author = Author.objects.get(id=author_id)
        except:
            print("Author not found.")
            return None
        github_url = author.github
        try:
            github_username = github_url.split("/")[3]
        except:
            print("Github url is wrong format.")
            return {}
        request_url = "https://api.github.com/users/" + github_username + "/events/public"
        response = requests.get(request_url)
        json_data = json.loads(response.text)

        events = []
        for data in json_data:
            if (data["type"] == "GollumEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                pages = payload["pages"][0]
                event_string = display_name + " " + pages["action"] + " " + pages["page_name"]

                event["event_message"] = event_string
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

            elif (data["type"] == "CreateEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                repo = data["repo"]
                if (payload["ref"] != None):
                    event_string = display_name + " created " + payload["ref_type"] + " " + payload["ref"] + " on " + repo["name"]
                else:
                    event_string = display_name + " created " + payload["ref_type"] + " " + repo["name"]

                event["event_message"] = event_string
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

            elif (data["type"] == "IssuesEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                issue = payload["issue"]
                event_string = "{} {} {}".format(display_name, payload["action"], issue["title"])

                event["event_message"] = event_string
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

            elif (data["type"] == "IssueCommentEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                issue = payload["issue"]
                comment = payload["comment"]
                event_string = "{} {} comment \"{}\" on issue {}".format(display_name, payload["action"], comment["body"], issue["title"])

                event["event_message"] = event_string
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

            elif (data["type"] == "PullRequestEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                pull_request = payload["pull_request"]
                event_string = "{} {} pull request \"{}\"".format(display_name, payload["action"], pull_request["title"])

                event["event_message"] = event_string
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

            elif (data["type"] == "PushEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                commits = payload["commits"]
                commit_messages = ""
                for commit in commits:
                    commit_messages += "{} commited \"{}\"\n".format(display_name, commit["message"])
                formatted = commit_messages.strip()

                event["event_message"] = formatted
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

            elif (data["type"] == "DeleteEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                event_string = "{} deleted {} \"{}\"".format(display_name, payload["ref_type"], payload["ref"])

                event["event_message"] = event_string
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

            elif (data["type"] == "ForkEvent"):
                event = {"event_message": None, "avatar_url": None}
                actor = data["actor"]
                display_name = actor["display_login"]
                avatar_url = actor["avatar_url"]

                payload = data["payload"]
                repo = data["repo"]
                event_string = "{} forked \"{}\"".format(display_name, repo["name"])

                event["event_message"] = event_string
                event["avatar_url"] = avatar_url
                event["published"] = data["created_at"]
                events.append(event)

        return events




# Create your views here.

# api for /author
class AuthorAPI(APIView):
    model = Author

    def get(self, request,*args, **kwargs):
        authorId = kwargs['pk']
        response = {"query":'author'}
        try:
            current_user = Author.objects.get(id=authorId)
            # current requested user is on local
            #if ApiHelper.local_author(current_user, request.get_host()):

            # get current user's data. Note that friends' data is excluded
            author_data = ExtendAuthorSerializers(current_user).data

            # append each data to response
            for i in author_data.keys():
                response[i] = author_data[i]
            #friends = ApiHelper.get_friends(current_user)
            local_frds, foreign_frds = ApiHelper.update_friends(current_user, request.get_host())
            friends = local_frds + foreign_frds
            # append friend's detailed information to response
            response['friends'] = []
            for friend in friends:
                friend_data = Helper_AuthorSerializers(Author.objects.get(id=friend)).data
                response['friends'].append(friend_data)
            return Response(response, status=200)
            #else:
            #    response, code = ApiHelper.get_from_remote_server(current_user)
            #    return Response(response, status=code)
        except:
            # Todo: might need to change this
            response['authors'] = []
            return Response(response, status=404)


# /unfriendrequest
# getting POST request from client. Un-friend given initiator and receiver.
class UnfriendRequestHandler(APIView):
    #Authentication
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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

        #case that when unfriend friend object is from foreign server
        if not ApiHelper.local_author(recv_user.host, request.get_host()):
            reverse_friendship = Friendship.objects.filter(init_id=recv_user, recv_id=init_user) # pylint: disable=maybe-no-member
            friendship = Friendship.objects.filter(init_id=init_user, recv_id=recv_user) # pylint: disable=maybe-no-member
            friendship.delete()
            reverse_friendship.delete()
            response['success'] = True
            response['message'] = 'Unfriend request proceeded successfully.'
            return Response(response)

        # try to delete the relationship with given init_user and recv_user
        reverse_friendship = Friendship.objects.filter(init_id=recv_user, recv_id=init_user) # pylint: disable=maybe-no-member
        friendship = Friendship.objects.filter(init_id=init_user, recv_id=recv_user) # pylint: disable=maybe-no-member
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
    #Authentication
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        is_local = ApiHelper.is_local_request(request)
        if is_local:
            reqUsrId = request.user.id
            try:
                reqAuthor = Author.objects.get(pk=reqUsrId)
                requestList = ApiHelper.get_all_friend_requests(reqAuthor)
                response = {'query': 'friendrequest_count',
                            'counts': len(requestList)}
                return Response(response)
            except:
                pass
        return Response(status=status.HTTP_403_FORBIDDEN)

    def post(self, request):
        is_local = ApiHelper.is_local_request(request)
        # parse request body
        request_body = request.data
        # response body
        response = {"query":'friendrequest'}

        # instanciate initiator and receiver as Author object
        send_id = request_body['author']['id'].replace(request_body['author']['host']+'/author/','')
        rcv_id = request_body['friend']['id'].replace(request_body['friend']['host']+'/author/','')

        if is_local:
            #reqeust from local user
            friend_host = request_body['friend']['host'].rstrip('/')
            frd_req_url = friend_host + '/friendrequest'

            try:
                init_user = Author.objects.get(id=send_id)
            except:
                response['success'] = False
                response['message'] = 'Request author does not exist.'
                return HttpResponse(json.dumps(response), status=404)

            try:
                recv_user = Author.objects.get(id=rcv_id)
            except:
                #request friend user is not on local database
                if ApiHelper.local_author(friend_host, request.get_host()):
                    #request friend user is from local server
                    response['success'] = False
                    response['message'] = 'Request friends does not exist.'
                    return HttpResponse(json.dumps(response), status=404)
                else:
                    #request friend user is from remote server
                    response, status_code = ApiHelper.obtain_from_remote_node(url=frd_req_url,
                        host=friend_host, method='POST', send_query=json.dumps(request_body))
                    if status_code == 200:
                        #create remote author object
                        success, recv_user = ApiHelper.create_remote_author(request_body['friend'])
                        #add following status if atuhor is created successfully
                        if success:
                            friendship = Friendship(init_id=init_user, recv_id=recv_user,
                                state=1, starting_date=datetime.datetime.now())
                            friendship.save()
                        else:
                            response = {"query": 'friendrequest'}
                            response['success'] = False
                            response['message'] = 'Failed to create remote author on server'
                            return Response(response, status=500)

                    return Response(response, status=status_code)
            else:
                #request friend user is on local database
                try:
                    friendship = Friendship.objects.get(init_id=init_user, recv_id=recv_user)
                except:
                    reverse_friendship = Friendship.objects.filter(init_id=recv_user, recv_id=init_user) # pylint: disable=maybe-no-member
                    friendship = Friendship(init_id=init_user, recv_id=recv_user, starting_date=datetime.datetime.now())

                    if ApiHelper.local_author(friend_host, request.get_host()):
                        #request friend user is from local server
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
                    else:
                        #request friend user is from remote server
                        response, status_code = ApiHelper.obtain_from_remote_node(url=frd_req_url,
                            host=friend_host, method='POST', send_query=json.dumps(request_body))

                        if status_code == 200:
                            #remote friend request is sent successfully, set init_id following recv_id
                            if reverse_friendship.exists():
                                reverse_friendship.update(state=1, starting_date=datetime.datetime.now())
                            friendship.state = 1
                            friendship.save()
                            response = {"query": 'friendrequest'}
                            response['success'] = True
                            response['message'] = 'Your friend request is sent successfully.'
                            return Response(response, status=200)

                        return Response(response, status=status_code)
                else:
                    #friend request is sent already or init_user is already followed to recv_user
                    response['message'] = 'You are already followed this user.'
                    return HttpResponse(json.dumps(response), status=404)
        else:
            # request from foreign host
            try:
                recv_user = Author.objects.get(id=rcv_id)
            except:
                response['success'] = False
                response['message'] = "Friend with id: {} does not exist".format(rcv_id)
                return Response(response, status=status.HTTP_404_NOT_FOUND)

            try:
                init_user = Author.objects.get(id=send_id)
            except:
                #remote user does not exists on local db, create a new author on it
                success, init_user = ApiHelper.create_remote_author(request_body['author'])
                #add following status if atuhor is created successfully
                if success:
                    friendship = Friendship(init_id=init_user, recv_id=recv_user,
                        state=0, starting_date=datetime.datetime.now())
                    friendship.save()
                    response['success'] = True
                    response['message'] = 'Friendrequest is sent successfully'
                    return Response(response, status=200)
                else:
                    response['success'] = False
                    response['message'] = 'Failed to create remote author on server'
                    return Response(response, status=500)
            else:
                #remote user exists on local db
                try:
                    friendship = Friendship.objects.get(init_id=init_user, recv_id=recv_user)
                except:
                    friendship = Friendship(init_id=init_user, recv_id=recv_user, starting_date=datetime.datetime.now())
                    reverse_friendship = Friendship.objects.filter(init_id=recv_user, recv_id=init_user)  # pylint: disable=maybe-no-member

                    if reverse_friendship.exists():
                        reverse_friendship.update(state=1, starting_date=datetime.datetime.now())
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
                else:
                    #friend request is sent already or init_user is already followed to recv_user
                    response['message'] = 'You are already followed this user.'
                    return HttpResponse(json.dumps(response), status=404)


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
    #Authentication
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    # get a list of ids who is friend of given user.
    def get(self, request,*args, **kwargs):
        is_local = ApiHelper.is_local_request(request)
        response = {"query":'friends'}

        try:
            # get current user on URL
            current_user = Author.objects.get(id=kwargs['pk'])
            if is_local:
                # current requested user is on local
                local_frds, foreign_frds = ApiHelper.update_friends(current_user, request.get_host())
                friends = local_frds + foreign_frds
                response['authors'] = friends
                return Response(response)
            else:
                # current requested user is from remote server
                friends = ApiHelper.get_friends(current_user)
                friends = [author.url for author in Author.objects.filter(id__in=friends)]
                response['authors'] = friends
                return Response(response)
        except Exception as e:
            print('author/id/friends exception: ', e)
            response['authors'] = []
            return Response(response, status=400)

    # Ask a service if anyone in the list is a friend
    def post(self, request,*args, **kwargs):
        is_local = ApiHelper.is_local_request(request)
        # parse request body
        request_body = json.loads(request.body.decode())

        # get the authors who are checked be a friend of author shows in URL
        request_friends = ApiHelper.urls_to_ids(request_body['authors'])
        #request_friends = request_body['authors']

        response = {"query":'friends',
                    "author": request_body['author']}
                    
        try:
            # get current user on URL
            current_user = Author.objects.get(id=kwargs['pk'])

            friends = ApiHelper.get_friends(current_user)
            #friends = Author.objects.filter(id__in=friends)
            response['authors'] = []
            for friend in friends:
                if friend in request_friends:
                    response['authors'].append(friend)
            return Response(response)
        except:
            response['authors'] = []
            return Response(response, status=400)

#reference: https://docs.djangoproject.com/en/2.1/ref/request-response/

# service/author/<authorid>/friends/<authorid>
# Todo: handle remote part
class TwoAuthorsRelation(APIView):
    #Authentication
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

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
            return Response(response, status=400)

# service/author/posts
class AuthorPostsAPI(APIView):
    #Authentication
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        print("=============")
        is_local = ApiHelper.is_local_request(request)
        allposts = []
        page_size = 1000
        posts = Post.objects.none() # pylint: disable=maybe-no-member

        if not ApiHelper.is_sharePosts(is_local, request.user):
            return Response(status=403)

        #get all public posts
        public = Post.objects.filter(visibility="PUBLIC", unlisted=False)   # pylint: disable=maybe-no-member
        posts |= public

        try:
            foreign_posts = list()
            if is_local:
                # request from local user
                current_user = Author.objects.get(pk=request.user.id)
                #get all visible posts from remote server(s)
                for node in Node.objects.all():
                    posts_url = node.foreignHost + '/author/posts'
                    header = {'X-Request-User-ID': current_user.host+'/author/'+str(current_user.id),
                            'X-UUID': str(current_user.id)}
                    query_posts, status_code = ApiHelper.obtain_from_remote_node(url=posts_url, host=node.foreignHost, header=header)
                    if status_code == 200:
                        foreign_posts += query_posts['posts']
            else:
                request_user_id = request.META.get('HTTP_X_REQUEST_USER_ID', '')
                request_user_id = ApiHelper.urls_to_ids([request_user_id])[0]
                current_user = Author.objects.get(pk=request_user_id)
        except Exception as e:
            print("Exception on author/posts: ", e)
            return Response(ApiHelper.format_author_posts(posts))

        local_frds, foreign_frds = ApiHelper.update_friends(current_user, request.get_host())
        friends = local_frds + foreign_frds
        #get posts mde by current user
        posts |= Post.objects.filter(postauthor=current_user, unlisted=False)  # pylint: disable=maybe-no-member

        allfoafs = set()
        visible_post = list()
        for friend in friends:
            friend = Author.objects.get(pk=friend)
            if not ApiHelper.local_author(friend.host, request.get_host()):
                continue

            # get friend's posts
            newposts = Post.objects.filter(postauthor = friend, visibility = "FRIENDS", unlisted=False) # pylint: disable=maybe-no-member
            posts |= newposts

            # get relations that satisfy FOAF
            # direct friend with posts "FOAF" should visible to current user
            allfoafs.add(friend)
            foafs = ApiHelper.get_friends(friend)
            for each in foafs:
                try:
                    author = Author.objects.get(id=each)
                    if ApiHelper.local_author(author.host, request.get_host()):
                        allfoafs.add(each)
                except:
                    pass

            #private
            newposts = Post.objects.filter(postauthor=friend, visibility="PRIVATE", unlisted=False)  # pylint: disable=maybe-no-member
            for post in newposts:
                if str(current_user.id) in post.visibleTo:
                    visible_post.append(post.postid)

            #get SERVERONLY
            if is_local:
                posts |= Post.objects.filter(postauthor=friend, visibility="SERVERONLY", unlisted=False)

        # get posts that satisfy FOAF
        for foaf in allfoafs:
            newposts = Post.objects.filter(visibility="FOAF", postauthor=foaf, unlisted=False) # pylint: disable=maybe-no-member
            posts |= newposts
        #get all private which can fullfill condition
        posts |= Post.objects.filter(postid__in=visible_post)  # pylint: disable=maybe-no-member

        if not ApiHelper.is_shareImgs(is_local, request.user):
            posts = posts.exclude(Q(contentType='image/png;base64') |
                          Q(contentType='image/jpeg;base64'))

        allposts = foreign_posts
        for post in posts:
            serializer = PostSerializer(post).data
            serializer['id'] = str(serializer['id'])
            allposts.append(serializer)

        #order post py bublished date
        allposts = sorted(allposts, key=lambda x: x['published'], reverse=True)

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

        response['posts'] = response_posts
        # for post in response_posts:
        #     serializer = PostSerializer(post).data
        #     serializer['postid'] = str(serializer['postid'])
        #     response['posts'].append(serializer)

        return Response(response)
    def post(self, request):
        # POST: Create a post
        is_local = is_local = ApiHelper.is_local_request(request)
        if is_local:
            curAuthor = Author.objects.get(id=request.user.id)
            origin = request.scheme+ "://" +request.get_host()+ "/"
            serializer = PostSerializer(data=request.data, context={'author': curAuthor, 'origin': origin})
            if serializer.is_valid():
                serializer.save()
                #Todo: response success message on json format
                return Response()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
# for author/{author_id}/madeposts
class AuthorMadePostAPI(APIView):
    def get(self,request,pk):
        if request.user.id == pk:
            try:
                response = {}
                response['query'] = "madeposts"
                author = Author.objects.get(pk=pk)
                posts = Post.objects.filter(postauthor = author).order_by(F("published").desc())   # pylint: disable=maybe-no-member
                serializer = PostSerializer(posts, many=True)
                response['posts'] = serializer.data
                response['count'] = len(serializer.data)
                return Response(response, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)


# author/{author_id}/posts
class ViewAuthorPostAPI(APIView):
    #Authentication
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        print("==================")
        is_local = ApiHelper.is_local_request(request)
        allposts = []
        page_size = 1000
        valid_req_user_id = True
        FOAF = False
        posts = Post.objects.none() # pylint: disable=maybe-no-member

        if not ApiHelper.is_sharePosts(is_local, request.user):
            return Response(status=403)

        try:
            author_be_viewed = Author.objects.get(pk=pk)
            #get all public posts of author be viewed
            posts |= Post.objects.filter(postauthor=author_be_viewed, visibility="PUBLIC", unlisted=False)  # pylint: disable=maybe-no-member

            if is_local:
                # request from local user
                current_user = Author.objects.get(pk=request.user.id)
            else:
                request_user_id = request.META.get('HTTP_X_REQUEST_USER_ID', '')
                request_user_id = ApiHelper.urls_to_ids([request_user_id])[0]
                current_user = Author.objects.get(pk=request_user_id)
        except Exception as e:
            print("Exception on author/posts: ", e)
            valid_req_user_id = False

        if valid_req_user_id:
            if current_user == author_be_viewed:
                posts = Post.objects.filter(postauthor=current_user, unlisted=False)    # pylint: disable=maybe-no-member
            else:
                local_frds, foreign_frds = ApiHelper.update_friends(current_user, request.get_host())
                friends = local_frds + foreign_frds
                visible_post = list()
                if str(author_be_viewed.id) in friends:
                    # get posts which set to FRIEND
                    posts |= Post.objects.filter(postauthor=author_be_viewed, visibility="FRIENDS", unlisted=False)  # pylint: disable=maybe-no-member
                    #private
                    private_posts = Post.objects.filter(postauthor=author_be_viewed, visibility="PRIVATE", unlisted=False)
                    for post in private_posts:
                        if str(current_user.id) in post.visibleTo:
                            visible_post.append(post.postid)
                    #get SERVERONLY
                    if is_local:
                        posts |= Post.objects.filter(postauthor=author_be_viewed, visibility="SERVERONLY", unlisted=False)
                    #case: direct friend, get foaf
                    posts |= Post.objects.filter(postauthor=author_be_viewed, visibility="FOAF", unlisted=False)
                    FOAF = True
                #get posts in visible_post list
                posts |= Post.objects.filter(postid__in=visible_post)
                #check visibility of FOAF if author be viewed is not a friend with current user
                if not FOAF:
                    foaf_posts = Post.objects.filter(postauthor=author_be_viewed, visibility="FOAF", unlisted=False)
                    if foaf_posts.exists() and ApiHelper.permission_on_foaf(current_user, author_be_viewed, is_local):
                        posts |= foaf_posts

        if not ApiHelper.is_shareImgs(is_local, request.user):
            posts = posts.exclude(Q(contentType='image/png;base64') |
                                  Q(contentType='image/jpeg;base64'))

        posts = posts.order_by(F("published").desc())
        for post in posts:
            allposts.append(post)

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
            response['previous'] = author_be_viewed.host + "/author/posts?page="+str(page-1)

        if(not last_page):
            response['next'] = author_be_viewed.host + "/author/posts?page="+str(page+1)

        response['posts'] = []
        for post in response_posts:
            serializer = PostSerializer(post).data
            serializer['id'] = str(serializer['id'])
            response['posts'].append(serializer)
        return Response(response)
