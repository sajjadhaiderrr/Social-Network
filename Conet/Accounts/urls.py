from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.SignUpPage.as_view(), name='signup'),
]