from django.test import TestCase,Client
from fb.models import CustomUser
from fb.classviews import *
from django.urls import reverse

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core import mail
from django.contrib.auth.hashers import check_password

User = get_user_model()

class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup') 
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.home_url = reverse('home')

        self.user_data = {
            'firstname': 'John',
            'lastname': 'Doe',
            'Date_of_birth':'2000-04-12',
            'gender':'Male',
            'email': 'johndoe@gmail.com',
            'phone_number': '9981979637',
            'password': 'Asdf@123'
        }

    def test_signup_get(self):
        response = self.client.get(self.signup_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fb/signup.html')



    # def test_signup_post_valid(self):
    #     response = self.client.post(self.signup_url,self.user_data)
    #     self.assertRedirects(response, self.login_url)

        # self.assertEqual(User.objects.count(), 1)
        # user = User.objects.first()
        # self.assertEqual(user.email, self.user_data['email'])
        # self.assertTrue(check_password(self.user_data['password'], user.password))

    def test_signup_post_invalid(self):
    	invalid_data=self.user_data.copy()
    	invalid_data['email']=''
    	response=self.client.post(self.signup_url,invalid_data)
    	self.assertEqual(response.status_code,200)
    	self.assertFormError(response,'form','email','This field is required.')

    def test_login_get(self):
    	response=self.client.get(self.login_url)
    	self.assertEqual(response.status_code,200)
    	self.assertTemplateUsed(response,'fb/login.html')

    def test_login_post_valid(self):
    	user=User.objects.create_user(phone_number=self.user_data['phone_number'],password=self.user_data['password'])
    	response=self.client.post(self.login_url,{'phone_number':self.user_data['phone_number'],'password':self.user_data['password']})
    	self.assertRedirects(response,self.home_url)
    	self.assertTrue('_auth_user_id' in self.client.session)
    
    def test_login_post_invalid(self):
    	response=self.client.post(self.login_url,{'phone_number':'11111111','password':'tttt'})
    	self.assertEqual(response.status_code,200)
    	self.assertFormError(response,'form',None,'Invalid')


    def test_logout(self):
    	user=User.objects.create_user(phone_number=self.user_data['phone_number'],password=self.user_data['password'])
    	self.client.login(phone_number=self.user_data['phone_number'], password=self.user_data['password'])
    	response=self.client.get(self.logout_url)
    	self.assertRedirects(response,self.login_url)


class HomePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(firstname='Arpita', password='Asdf@123')
        self.profile = UserProfile.objects.create(user=self.user)
        self.home_url = reverse('home')
    
    def test_home_page_get_authenticated(self):
        self.client.login(phone_number='8827489124', password='Asdf@123')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code,302)
        # self.assertTemplateUsed(response, 'home.html')
        # self.assertIn('posts', response.context)
        # self.assertIn('users', response.context)






















#     def test_home_page_get_authenticated(self):
#         self.client.login(username='testuser', password='pass')
#         response = self.client.get(self.home_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home.html')
#         self.assertIn('posts', response.context)
#         self.assertIn('users', response.context)

#     def test_home_page_redirect_if_not_logged_in(self):
#         response = self.client.get(self.home_url)
#         self.assertNotEqual(response.status_code, 200)
#         self.assertRedirects(response, f'/accounts/login/?next={self.home_url}')

#     def test_home_page_post_create_text_post(self):
#         self.client.login(username='testuser', password='pass')
#         response = self.client.post(self.home_url, {'content': 'My first post'})
#         self.assertEqual(response.status_code, 302)
#         self.assertTrue(CreatePost.objects.filter(user=self.profile, content='My first post').exists())

#     def test_home_page_post_create_image_post(self):
#         self.client.login(username='testuser', password='pass')
#         image = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
#         response = self.client.post(self.home_url, {'image': image})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(CreatePost.objects.count(), 1)
#         self.assertIsNotNone(CreatePost.objects.first().image)

#     def test_home_page_post_empty_content_image(self):
#         self.client.login(username='testuser', password='pass')
#         response = self.client.post(self.home_url, {'content': '', 'image': ''})
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(CreatePost.objects.count(), 0)


