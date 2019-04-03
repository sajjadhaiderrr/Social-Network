from rest_framework.response import Response
from posting.models import Post, Comment
from Accounts.models import Author, Node
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .post_api import CheckPermissions


''' VERIFICATION HELPER START'''

# Verify if the current user has access to post
def currentPostUserVerification(post, request):
    author = post.author_id
    visibility = post.visibility
    unlisted = post.unlisted
    if Author.objects.filter(pk=request.user.id).exists():
        user = Author.objects.get(pk=request.user.id)
        # TODO: Check if user is friends with poster
        if user == author:
            return True
        else:
            if visibility == 'PUBLIC':
                return True
            elif visibility == 'FOAF':
                return True
            #TODO: Check for friend
            elif visibility == 'PRIVATE':
                if user == author:
                    return True
                elif post.visibleTo is not None:
                    if (str(user) in post.visibleTo):
                        return True
                    else:
                        return False
                else:
                    return False
            #TODO: SERVER ONLY
            else:
                    return False
    elif (not User.objects.filter(pk=request.user.id).exists()):
        return False


''' VERIFICATION HELPER END'''


'''VIEW HELPER START'''
def createPost(request):
    return render(request, "createpost.html")

def editPost(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, "editpost.html", {'post': post})

def viewPost(request, post_id):
    url = request.GET['host']+"/post/"+ str(post_id)
        
    #user_be_viewed={"id":authorId, "host":request.GET['host'], "url":url, "displayName":"abc"}
    host = request.GET['host'][7:]
    remote = {}
    # need to merge
    if(request.get_host() == host):
        remote['host'] = host
        from_one_host = True
    else:
        from_one_host = False
        node = Node.objects.get(foreignHost=request.GET['host'])
        remote['host'] = host
        remote['username'] = node.remoteUsername
        remote['password'] = node.remotePassword
    response = render(request, "viewpost.html", \
               {'post_url': url,\
                'remote': remote, \
                'from_one_host': from_one_host, \
                'request_user_id': request.user.id})
    #print("good for now")
    return response
''' VIEW HELPER END '''