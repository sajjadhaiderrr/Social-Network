from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path('friendrequest/', views.friend_request, name='friendrequest'),
    path('unfriendrequest/', views.unfriend_request, name='friendrequest'),
    path('author/<uuid:pk>/friends/', csrf_exempt(views.AuthorFriends.as_view()), name='authorfriends')
]