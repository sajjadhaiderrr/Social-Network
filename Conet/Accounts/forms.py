from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from .models import Author


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Author
        fields = ['username','first_name', 'last_name', 'email', 'displayName', 'github']


class SearchUserForm(forms.Form):
    user_name = forms.CharField(max_length=100)