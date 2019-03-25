from django.urls import path
from . import post_api, views, Helper

urlpatterns = [
    ### HELPER START

    path('api/posts', post_api.PostReqHandler.as_view(), name='view_posts'),
    path('api/comments', post_api.CommentReqHandler.as_view(), name='view_comments'),
    path('create/', Helper.createPost, name='create_post'),
    path('view/', Helper.viewPost, name='post_details'),

    ### HELPER END


    ### API START

    path('', post_api.PostReqHandler.as_view(), name='view_public_posts'),
    path('<post_id>', post_api.ReadSinglePost.as_view(), name='view_post'),
    path('<post_id>/comments', post_api.ReadAndCreateAllCommentsOnSinglePost.as_view(), name='view_posts'),

    ### API END
]
