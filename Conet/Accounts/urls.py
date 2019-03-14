from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUpPage.as_view(), name='signup'),
    path('<uuid:pk>/', views.ProfilePage.as_view(), name='profile'),
    path('searchresult/', views.SearchResultPage.as_view(), name='searchresult')
    #path('<uuid:pk>/friendrequest')
]