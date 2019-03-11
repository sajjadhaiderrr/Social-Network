from django.urls import path
from . import post_api, views, Helper

urlpatterns = [
    path('', post_api.PostWithoutIdReqHandler.as_view(), name='view_posts'),
    path('create/', Helper.createPost, name='create_post'),
    path('view/', Helper.viewPost, name='view_post'),
    #path('', post_api.PostWithoutIdReqHandler.as_view()),
    #path('<postid>/', post_api.PostWithIdReqHandler.as_view()),
    #path('<postid>/comments', post_api.CommentReqHandler.as_view()),
]
