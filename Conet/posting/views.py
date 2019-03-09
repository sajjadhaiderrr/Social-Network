from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from posting.models import Post, Comment
from posting.serializers import PostSerializer
from django.shortcuts import render


# Create your views here.
class postReqHandler(APIView):

    def get(self, request, postid):
        return
    def post(self, request):
        return
    def put(self, request):
        return
    def delete(self, request, postid):
        return
