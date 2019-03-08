from django.urls import path
from . import views

urlpatterns = [
    path('', views.post),
    path('<postid>/', views.post),
    path('<postid>/comments', views.comment),
]