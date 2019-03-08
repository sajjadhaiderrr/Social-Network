from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('friendrequest/', views.friend_request, name='friendrequest'),
    path('unfriendrequest/', views.unfriend_request, name='friendrequest'),
]