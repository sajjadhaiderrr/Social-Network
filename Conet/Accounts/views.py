from django.shortcuts import render, redirect
from .models import Author
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views import View
from django.http import HttpResponse
from .forms import SignUpForm, SearchUserForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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
            user.url = user.host + "/" + str(user.id) + '/'
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
        search_form = self.search_form()
        return render(request, self.template_name, {'search_form': search_form, 'user_be_viewed':user_be_viewed})
    
    # receive a POST from search box
    def post(self, request, *args, **kwargs):
        user_be_viewed = Author.objects.get(pk=request.get_full_path().split("/")[2])
        current_user = request.user

        # if you are viewing your own website
        if (user_be_viewed.id == current_user.id):
            search_form = self.search_form(request.POST)
            # get the user name from input box, 
            if search_form.is_valid():
                user_to_search = search_form.cleaned_data['user_name']
            return HttpResponse(user_to_search)

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


def send_friend_request(request, *args, **kwargs):
    print(request)
