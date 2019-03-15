import datetime
import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View, generic
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .forms import SearchUserForm, SignUpForm
from .models import Author, Friendship


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
            form.save()
            user = Author.objects.get(username=username)
            user.host = 'http://'+request.META['HTTP_HOST']
            user.url = user.host + "/author/" + str(user.id) + '/'
            user.save()
            return redirect(self.success_url)
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
    def get(self, request, *args, **kwargs):
        # get current user and user that is being viewed
        user_be_viewed = Author.objects.get(pk=request.get_full_path().split("/")[2])
        current_user = request.user
        if(current_user != user_be_viewed):
            return HttpResponseRedirect(user_be_viewed.url+"info/")
        return render(request, self.template_name, {'user_be_viewed':user_be_viewed})
            

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

class InfoPage(View):
    template_name = 'Accounts/info.html'
    
    def get(self, request, *args, **kwargs):
        user_be_viewed = Author.objects.get(id=kwargs['pk'])
        
        return render(request, self.template_name, {'user_be_viewed':user_be_viewed})

class FriendsPage(View):
    template_name = 'Accounts/friendslist.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{})