from django.test import TestCase,Client
from fb.models import CustomUser
from fb.classviews import *
from django.urls import reverse

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.auth.hashers import check_password

class SocialMediaViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.create_user(firstname='sonam',lastname='patidar',Date_of_birth="2000-09-12",gender="female",email="sonam@gmail.com",phone_number='8827489124', password='Asdf@123')
        self.user2 = CustomUser.objects.create_user(firstname='rahul',lastname='patidar',Date_of_birth="2000-08-23",gender="male",email="Rahul@gmail.com",phone_number='8827489136', password='Asdf@123')
        self.user1_profile = UserProfile.objects.create(user=self.user1)
        self.user2_profile = UserProfile.objects.create(user=self.user2)
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.client.login(phone_number='8827489124', password='Asdf@123')

    def test_home_page_get(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_create_post(self):
        response = self.client.post(self.home_url, {'content': 'Test post'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CreatePost.objects.filter(content='Test post').exists())

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'firstname': 'kajal',
            'lastname': 'patidar',
            'email': 'kajal12@example.com',
            'phone_number': '8827489120',
            'password': 'Asdf@123',
            'Date_of_birth': '2000-01-01'
        })
        self.assertEqual(response.status_code, 200 or 302)

    def test_login_view(self):
        self.client.logout()
        response = self.client.post(self.login_url, {'phone_number': '8827489123', 'password': 'Asdf@123'})
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_profile_view(self):
        url = reverse('profile', args=[self.user2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fb/profile.html')

    def test_like_view(self):
        post = CreatePost.objects.create(user=self.user2_profile, content='Like this')
        response = self.client.post(reverse('likepost', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, post.likes.all())

    def test_comment_view(self):
        post = CreatePost.objects.create(user=self.user2_profile, content='Post')
        response = self.client.post(reverse('commen', args=[post.id]), {
            'text': 'Nice post!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(text='Nice post!').exists())

    def test_send_friend_request(self):
        response=self.client.get(reverse('send_friend_request',args=[self.user2.id]))
        self.assertEqual(response.status_code,302)
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1,to_user=self.user2).exists())

    def test_accept_friend_request(self):
        friend_request=FriendRequest.objects.create(from_user=self.user2,to_user=self.user1)
        response=self.client.get(reverse('accept_friend_request',args=[friend_request.id]))
        self.assertEqual(response.status_code,302)
        self.assertFalse(FriendRequest.objects.filter(id=friend_request.id).exists())
        self.assertTrue(Follow.objects.filter(follower=self.user1,followed=self.user2).exists())
    
    def test_show_friend_request(self):
        response=self.client.get(reverse('show_friends',args=[self.user1.id]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'send_request.html')

    def test_followers_list(self):
        response=self.client.get(reverse('followers_list',args=[self.user1.id]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'followers_list.html')


    def test_following_list(self):
        response=self.client.get(reverse('following_list',args=[self.user1.id]))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'following_list.html')


    def test_edit_profile(self):
        response=self.client.get(reverse('edit_profiles'))
        self.assertEqual(response.status_code,200)
        self.assertTrue(response,'edit_profile.html')

    def test_edit_profile_post(self):
        response=self.client.post(reverse('edit_profiles'),{'bio':'Updated bio'})
        self.assertEqual(response.status_code,302)
        self.assertEqual(UserProfile.objects.get(user=self.user1).bio,'Updated bio')

    def test_userpost(self):
        response=self.client.get(reverse('user_posts'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'user_posts.html')


    def test_Deletepost(self):
        post=CreatePost.objects.create(user=self.user1_profile,content="Deleted")
        response=self.client.post('delete_post',args=[post.id])
        self.assertEqual(response.status_code,404)
        self.assertTrue(CreatePost.objects.filter(id=post.id).exists())

    
    def text_show_comment_get(self):
        post=CreatePost.objects.create(user=self.user1_profile,content="comment here")
        response=self.client.get('morecomment',args=[post.id])
        self.assertEqual(response.status_code,200)

    def test_show_comment_post(self):
        post=CreatePost.objects.create(user=self.user1_profile,content="comment")
        response=self.client.post(reverse('morecomment',args=[post.id]),{'text':'Another comment'})
        self.assertEqual(response.status_code,302)
        self.assertTrue(Comment.objects.filter(text='Another comment').exists())

        

  

    
   

  

    

    

    # def test_post_comment_from_show_page(self):
    #     post = CreatePost.objects.create(user=self.user1_profile, content='Comment here')
    #     response = self.client.post(reverse('show_comments', args=[post.id]), {
    #         'content': 'Another comment'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(Comment.objects.filter(content='Another comment').exists())