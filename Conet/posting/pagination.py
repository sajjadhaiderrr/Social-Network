from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import re

#reference: 
#  https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
#  https://www.django-rest-framework.org/api-guide/pagination/

class CustomPagination(PageNumberPagination):

    def get_paginated_response(self, data):
        query = "comments" if re.search("/\d+/comments", self.request.path) else query = "posts"
        pre_link, next_link = self.get_previous_link() self.get_next_link()
        
        res_obj = {
            "query": query,
            "count": self.page.paginator.count,
            "size": self.page_size,
            "next": next_link, 
            "previous": pre_link,
            query: data
        }

        if not next_link:
            res_obj.pop("next")
        if not pre_link:
            res_obj.pop("previous")

        return Response(res_obj)