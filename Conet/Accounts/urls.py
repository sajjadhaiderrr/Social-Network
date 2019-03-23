from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUpPage.as_view(), name='signup'),
    path('<uuid:pk>/', views.ProfilePage.as_view(), name='profile'), #what is different between this
    path('searchresult/', views.SearchResultPage.as_view(), name='searchresult'),
    path('<uuid:authorId>/info/', views.InfoPage.as_view(), name='info'),#and this?
    path('<uuid:pk>/friends/', views.FriendsPage.as_view(), name='info'),
]