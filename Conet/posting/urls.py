from django.urls import path, include
from . import views, Helper

urlpatterns = [
    path('', views.CreatePostHandler.as_view(), name='view_posts')
    ,path('create/', Helper.createPost, name='create_post'),
    #, path('<postid>/', views.post),
    #path('<postid>/comments', views.comment),
]
