from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views


urlpatterns = [
    path('friendrequest/', views.friend_request, name='friendrequest'),
    path('unfriendrequest/', views.unfriend_request, name='friendrequest'),
    path('author/<uuid:pk>/following/', csrf_exempt(views.AuthorFollowing.as_view()), name='authorfollowing'),
    path('author/<uuid:pk>/follower/', csrf_exempt(views.AuthorFollower.as_view()), name='authorfollower'),
    path('author/<uuid:pk>/friends/', csrf_exempt(views.AuthorFriends.as_view()), name='authorfollowing'),
]