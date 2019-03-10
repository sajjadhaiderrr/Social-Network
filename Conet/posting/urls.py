from django.urls import path
from . import post_api

urlpatterns = [
    path('', post_api.PostWithoutIdReqHandler.as_view()),
    path('<postid>/', post_api.PostWithIdReqHandler.as_view()),
    path('<postid>/comments', post_api.CommentReqHandler.as_view()),
]