from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path('friendrequest', views.FriendRequestHandler.as_view(), name='friendrequest'),
    path('unfriendrequest', views.UnfriendRequestHandler.as_view(), name='unfriendrequest'),
    path('notification', views.notification, name="frdreq_notification"),
    path('author/<uuid:pk>/following', views.AuthorFollowing.as_view(), name='authorfollowing'),
    path('author/<uuid:pk>/follower', views.AuthorFollower.as_view(), name='authorfollower'),
    path('author/<uuid:pk>/friends', views.AuthorFriends.as_view(), name='authorfriends'),
    path('author/<uuid:pk>', views.AuthorAPI.as_view(), name='author'),
    path('author/<author_id1>/friends/<author_id2>', views.TwoAuthorsRelation.as_view(), name='two_authors_relation'),
    path('author/posts', views.AuthorPostsAPI.as_view(), name='authorizedposts'),
    path('author/<uuid:pk>/madeposts', views.AuthorMadePostAPI.as_view(), name='authormadeposts'),
    path('author/<uuid:pk>/posts', views.ViewAuthorPostAPI.as_view(), name='authoridposts'),

    path('author/<uuid:pk>/friends/', views.AuthorFriends.as_view()),
    path('author/<uuid:pk>/posts/', views.ViewAuthorPostAPI.as_view())
]
