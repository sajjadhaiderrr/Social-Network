import datetime
import json
from django.utils.six.moves.urllib.parse import urlsplit
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from .forms import SearchUserForm, SignUpForm
from .models import Author, Friendship, Node
from api.serializers import AuthorSerializer


# Signup page
class SignUpPage(View):
    form = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'Accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            formObj = form.save(commit=False)
            formObj.is_active = False
            formObj.save()
            user = Author.objects.get(username=username)
            user.host = 'http://'+request.META['HTTP_HOST']
            user.url = user.host + "/author/" + str(user.id)
            user.save()
            return HttpResponseRedirect(self.success_url)
        else:
            #form #= SignUpForm()
            return render(request, self.template_name, {'form': form})
    

# define the functions of home page
class ProfilePage(View):
    search_form = SearchUserForm
    success_url = reverse_lazy('home')
    template_name = 'Accounts/profile.html'
    model=Author

    # if a user is not loged-in, he/she will get redirected to login page
    @method_decorator(login_required(login_url='/author/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # if receive a GET request, create a new form
    def get(self, request, pk):
        # get current user and user that is being viewed
        scheme = urlsplit(request.build_absolute_uri(None)).scheme
        if (scheme=="https"):
            return HttpResponseRedirect('http://'+request.META['HTTP_HOST']+"/")
        user_be_viewed_id = pk
        current_user = request.user
        nodes = Node.objects.all()
        remote = []
        for node in nodes:
            remote_info = {}
            remote_info['host'] = node.foreignHost
            remote_info['username'] = node.remoteUsername
            remote_info['password'] = node.remotePassword
            remote.append(remote_info)

        if(str(current_user.id) != str(user_be_viewed_id)):
            return HttpResponseRedirect(403)
        return render(request, self.template_name, {'user_be_viewed_id':user_be_viewed_id, 'current_user':current_user, 'remote':remote})
            

class HomePage(View):
    search_form = SearchUserForm
    success_url = reverse_lazy('home')
    template_name = 'Accounts/home.html'
    user=Author

    # if a user is not loged-in, he/she will get redirected to login page
    @method_decorator(login_required(login_url='/author/login/'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    # if receive a GET request, create a new form
    def get(self, request, *args, **kwargs):
        url = reverse("profile", args=[request.user.id])
        return redirect(url)


class SearchResultPage(View):
    template_name = 'Accounts/searchresult.html'
    def get(self, request, *args, **kwarg):
        search_term = request.GET['search']
        authors = Author.objects.filter(displayName__contains=search_term).exclude(id=request.user.id)
        return render(request, self.template_name, {'authors':authors})


# Django: Add response header when using render or render_to_response
class InfoPage(APIView):
    template_name = 'Accounts/info.html'
    
    def get(self, request, authorId):
        #strip end / for remote server
        host = request.GET['host'].rstrip('/')
        url = host + "/author/"+ str(authorId)
        
        user_be_viewed={"id":authorId, "host":request.GET['host'], "url":url, "displayName":"abc"}
        remote = {}

        # need to merge
        if(request.get_host() in host):
            remote['host'] = host
            from_one_host = True
        else:
            from_one_host = False
            node = Node.objects.get(foreignHost=host)
            remote['host'] = host
            remote['username'] = node.remoteUsername
            remote['password'] = node.remotePassword

        from_one_author = True if(request.user.id == authorId) else False
        response = render(request, self.template_name, {'from_one_author': from_one_author,'user_be_viewed': user_be_viewed, 'remote': remote, 'from_one_host': from_one_host})
        return response

    def put(self, request, authorId):
        try:
            reqed_author = Author.objects.get(pk=authorId)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.user.id != authorId:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = AuthorSerializer(reqed_author, data=request.data)

        if serializer.is_valid():
            serializer.save()
            from_one_author = True
            return render(request, self.template_name, {'from_one_author':from_one_author, 'user_be_viewed':reqed_author})
        return Response(status=status.HTTP_400_BAD_REQUEST)

class FriendsPage(View):
    template_name = 'Accounts/friendslist.html'
    def get(self, request, authorId):

        host = request.GET['host'].rstrip('/')
        url = host + "/author/"+ str(authorId)

        user_be_viewed={"id":authorId, "host":request.GET['host'], "url":url, "displayName":"abc"}
        remote = {}

        # need to merge
        if(request.get_host() in host):
            remote['host'] = host
            from_one_host = True
        else:
            from_one_host = False
            node = Node.objects.get(foreignHost=host)
            remote['host'] = host
            remote['username'] = node.remoteUsername
            remote['password'] = node.remotePassword

        return render(request, self.template_name,{'query':'friends','remote':remote, 'user_be_viewed': user_be_viewed,'from_one_host':from_one_host})

class FollowersPage(View):
    template_name = 'Accounts/friendslist.html'
    def get(self, request, *args, **kwargs):
        user_be_viewed = Author.objects.get(id=kwargs['pk'])
        return render(request, self.template_name,{'query':'followers', 'user_be_viewed': user_be_viewed})

class FollowingPage(View):
    template_name = 'Accounts/friendslist.html'
    def get(self, request, *args, **kwargs):
        user_be_viewed = Author.objects.get(id=kwargs['pk'])
        return render(request, self.template_name,{'query':'following', 'user_be_viewed': user_be_viewed})
