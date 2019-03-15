from django.test import TestCase, Client
from django.urls import reverse
from posting.models import Post, Comment
from posting.serializers import PostSerializer, CommentSerializer
from Accounts.models import Author
import json

# Create your tests here.

class TestViews(TestCase):
 # https://stackoverflow.com/questions/2619102/djangos-self-client-login-does-not-work-in-unit-tests
 def setUp(self):
     # Base user
     self.user_base = User.objects.create(username="test1")
     self.user_base.set_password('test12345')
     self.user_base.save()

     self.client_base = Client()
     self.client_base.login(username="test1", password="test12345")

     self.author_base = Author.objects.create(user = self.user_base, displayName="tester1")

     # User to compare to
     self.user_comp = User.objects.create(username="test2")
     self.user_comp.set_password('test12345')
     self.user_comp.save()

     self.client_comp = Client()
     self.client_comp.login(username="test2", password="test12345")

     self.author_comp = Author.objects.create(user = self.user_comp, displayName="tester2")

     self.base_url = reverse('base')
     self.comp_url = reverse('comp')

def test_PostReqHandler(self):
    response = self.client_base.post(self.base_url,{
        'title':'testpost',
        'description':'testdescription',
        'categories':'testcategories',
        'contentType':'text/plain',
        'author':{ 'id':self.user.author_base, 'host':self.user.author_base.host, 'displayName':self.author_base.displayName},
        'visibility':'PUBLIC',
        'content':'test'
        },'application/json')
    self.assertEquals(response.status_code, 200)

# Test if post we create can be seen by other users if set to private
def test_PostReqHandler_PRIVATE_POST(self):
    response = self.client_base.post(self.base_url,{
        'title':'testpostprivate',
        'description':'testdescription',
        'categories':'testcategories',
        'contentType':'text/plain',
        'author':{ 'id':self.user.author_base, 'host':self.user.author_base.host, 'displayName':self.author_base.displayName},
        'visibility':'PRIVATE',
        'content':'test'
        },'application/json')
    self.assertEquals(response.status_code, 200)


    # Test if post we create can be seen by other users if set to private
    post_comp = Post.objects.get(tite='testpostprivate')
    post_comp_postid = post_comp.postid
    post_comp_url = reverse('edit', args[post_comp_postid])
    response = self.client.get(post_comp_url)
    self.assertEquals(response.status_code, 200)

    response_view = self.client_comp.get(post_comp_url)
    self.assertEquals(response.status_code, 404)

# Create a comment on a public post and check if the author of that post can see it
def test_CommentReqHandler(self):
    response = self.client_base.post(self.base_url,{
        'title':'testpostcomment',
        'description':'testdescription',
        'categories':'testcategories',
        'contentType':'text/plain',
        'author':{ 'id':self.user.author_base, 'host':self.user.author_base.host, 'displayName':self.author_base.displayName},
        'visibility':'PUBLIC',
        'content':'test'
        },'application/json')

    post = Post.objects.get(title='testpostcomment')
    post_id = post.postid

    comment_url = reverse('comment', args=[post_id])
    response = self.client_comp.post(comment_url, {
        'post':'testserver',
        'comment': {
        'author': { 'id': self.author_base.id  },
        'comment': 'testcomment'
        }
        },'application/json')

    response = self.client_base.get(comment_url)
    self.assertEquals(response.status_code,200)

    content = json.loads(response.content)
    self.assertEquals(content['comments'][0]['comment'],'testcomment')
