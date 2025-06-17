from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from fb.models import CustomUser, UserProfile, CreatePost, Comment
from rest_framework_simplejwt.tokens import RefreshToken

class APITestCases(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(firstname='kavi',lastname='patidar',email='kavi@gmail.com',phone_number='1234567890',password='Asdf@123')
        self.user2 = CustomUser.objects.create_user(firstname='rahul',lastname='patidar',email='rahul13@gmail.com',phone_number='9957643210',password='Asdf@123')
        self.profile1 = UserProfile.objects.create(user=self.user)
        self.profile2 = UserProfile.objects.create(user=self.user2)

        self.client.force_authenticate(user=self.user)


        self.post = CreatePost.objects.create(user=self.profile1, content='Hello World')
        self.comment = Comment.objects.create(user=self.user, post=self.post, text='Nice post')

        self.refresh = RefreshToken.for_user(self.user)

    def test_user_list_view(self):
        response=self.client.get(reverse('userapi'))
        self.assertEqual(response.status_code,200)

    def test_user_retrieve_view(self):
        response=self.client.get(reverse('userapi',kwargs={'pk':self.user.pk}))
        self.assertEqual(response.status_code,200)


    def test_user_update_view(self):
        response=self.client.put(reverse('userapi',kwargs={'pk':self.user.pk}))
        self.assertEqual(response.status_code,400)


    def test_user_delete_view(self):
        response=self.client.delete(reverse('userapi',kwargs={'pk':self.user.pk}))
        self.assertEqual(response.status_code,204)



    def test_user_registration(self):
        url = reverse('registration')
        data = {'phone_number': '7389971308','password': 'Asdf@123','firstname': 'Deepak','lastname': 'patidar','email': 'Deepak@gmail.com'}
    
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        url = reverse('loginapi')
        data = {'phone_number': '1234567890','password': 'Asdf@123'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_user_login_invalid(self):
        url=reverse('loginapi')
        data={'phone_number':'abc123','password':'Asdf@123'}
        response=self.client.post(url,data)
        self.assertEqual(response.status_code,401)

    def test_user_login_bad(self):
        url=reverse('loginapi')
        data={'phone_number':'','password':''}
        response=self.client.post(url,data)
        self.assertEqual(response.status_code,400)

    def test_logout_user(self):
        url = reverse('logoutapi')
        self.client.force_authenticate(user=self.user)
        data = {'refresh': str(self.refresh)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_logout_user_invalid(self):
        url=reverse('loginapi')
        data = {'refresh': str(self.refresh)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)



    def test_post_create_view(self):
        response=self.client.post(reverse('post-list'))
        self.assertEqual(response.status_code,201)


    def test_post_list_view(self):
        response=self.client.get(reverse('post-list'))
        self.assertEqual(response.status_code,200)

    # def test_post_update_view(self):
    #     response=self.client.put(reverse('post-detail',kwargs={'pk':self.post.pk}))
    #     self.assertEqual(response.status_code,405)


    def test_post_delete_view(self):
        response=self.client.delete(reverse('post-detail',kwargs={'pk':self.post.pk}))
        self.assertEqual(response.status_code,204)

   
    def test_comment_create_view(self):
        url=reverse('comment-list')
        response=self.client.post(url,{'post': self.post.id, 'text': 'Another comment'})
        self.assertEqual(response.status_code,201)


    def test_comment_get_view(self):
        response=self.client.get(reverse('comment-list'))
        self.assertEqual(response.status_code,200)


    def test_comment_delete_view(self):
        response=self.client.delete(reverse('comment-detail',kwargs={'pk':self.comment.pk}))
        self.assertEqual(response.status_code,204)
    