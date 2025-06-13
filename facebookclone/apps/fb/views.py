from django.shortcuts import render,redirect
from django.http.response import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import get_user_model
from .models import UserProfile  
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileForm
from django.contrib.auth.hashers import make_password ,check_password
from django.urls import reverse
from . import forms
from .forms import LoginForm
from .forms import post
# . refers to the current package or current directory where the views.py file is located.
from pathlib import Path
# from .backends import PhoneUsernameAuthenticationBackend as EoP

# User=get_user_model()


def home_page(request):
        posts = CreatePost.objects.all().order_by('-created_at')
        if request.method == 'POST':
            form = forms.CreatePostForm(request.POST, request.FILES)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.user = request.user.userprofile  
                new_post.save()
                return redirect('home')
        else:
            form = forms.CreatePostForm()
    
        return render(request, 'home.html', {
        'posts': posts,
        'form': form })



def logout_user(request):
    logout(request)
    return redirect('login')


def signup_page(request):
    form = forms.SignupForm()
    messages = ""
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        
        if form.is_valid():
            password = make_password(form.cleaned_data['password'])
            user = form.save()
            user.password = password  
            user.save()  
            return redirect('login')
    
    return render(request, 'signup.html', context={'form': form})


def login_page(request):
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            user = authenticate(request, phone_number=phone_number, password=password)
            
            if user is not None:
                login(request, user) 
                return redirect('home')  
            else:
                form.add_error(None, "Invalid credentials") 
    
    else:
        form = forms.LoginForm()
    
    return render(request, 'login.html', {'form': form})


def profile_page(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        form = None
    return render(request, 'profile.html', {'profile': form})


def post_page(request):
    return redirect('home')
        
def send_friendrequest(request):
    if request.method == 'POST':
        form = friends(request.POST)
        if form.is_valid():
            to_user_id = form.cleaned_data['to_user_id']

            if not str(to_user_id).isdigit():
                return redirect('home') 

            to_user = get_object_or_404(CustomUser, pk=to_user_id)
            # get_object_or_404=make sure we do not send a request to a non existing user

            if request.user == to_user:
                return redirect('profile_page', username=to_user.username)

            friend_request, created = Friend_request.objects.get_or_create(
                userfrom=request.user,
                to_user=to_user
            )
            # get_or_create=prevent dublicate request 
            

            return redirect('profile_page', username=to_user.username)
    
    return redirect('home')



def accept_request(request,requestid):
    friend_request=get_object_or_404(FriendRequest,id=request_id)
    if friend_request.to_user==request.user:
        friend_request.is_accepted=True
        friend_request.save()
    return redirect('friend_request')

def like_post(request, post_id):
    post = get_object_or_404(CreatePost, id=post_id)
    user = request.user

    like, created = Like.objects.get_or_create(post=post, liked_by=user)

    if not created:
        # User already liked, so remove it (unlike)
        like.delete()

    return redirect('home')  

 def test_home_page_get(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_post_create_post(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('home'), {'content': 'Test post'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CreatePost.objects.filter(content='Test post').exists())

    # ----------------- CREATE POST ------------------
    def test_create_post(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse('create_post'), {
            'content': 'Hello world!'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(CreatePost.objects.filter(content='Hello world!').exists())

    # ----------------- LIKE POST ------------------
    def test_like_post(self):
        self.client.force_login(self.user1)
        post = CreatePost.objects.create(user=self.profile1, content='Like me')
        response = self.client.post(reverse('like_post', args=[post.id]))
        self.assertEqual(response.status_code, 200)

    # ----------------- ADD COMMENT ------------------
    def test_add_comment(self):
        self.client.force_login(self.user1)
        post = CreatePost.objects.create(user=self.profile1, content='Comment here')
        response = self.client.post(reverse('add_comment', args=[post.id]), {
            'comment': 'Nice!',
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(Comment.objects.filter(post=post, comment='Nice!').exists())

    # ----------------- PROFILE PAGE ------------------
    def test_profile_page_get(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('profile_page', args=[self.user1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'fb/profile.html')

    # ----------------- SEND FRIEND REQUEST ------------------
    def test_send_friend_request(self):
        self.client.force_login(self.user1)
        response = self.client.get(reverse('send_friend_request', args=[self.user2.id]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())

    # ----------------- ACCEPT FRIEND REQUEST ------------------
    def test_accept_friend_request(self):
        self.client.force_login(self.user2)
        req = FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        response = self.client.get(reverse('accept_friend_request', args=[req.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FriendRequest.objects.filter(id=req.id).exists())
        self.assertTrue(Follow.objects.filter(follower=self.user1, followed=self.user2).exists())

    # ----------------- DELETE POST ------------------
    def test_delete_post_get_post(self):
        self.client.force_login(self.user1)
        post = CreatePost.objects.create(user=self.profile1, content='To be deleted')

        # GET request shows confirmation
        get_resp = self.client.get(reverse('delete_post', args=[post.id]))
        self.assertEqual(get_resp.status_code, 200)

        # POST request deletes the post
        post_resp = self.client.post(reverse('delete_post', args=[post.id]))
        self.assertEqual(post_resp.status_code, 302)
        self.assertFalse(CreatePost.objects.filter(id=post.id).exists())

    # ----------------- EDIT PROFILE ------------------
    def test_edit_profile_get_post(self):
        self.client.force_login(self.user1)

        get_resp = self.client.get(reverse('edit_profile'))
        self.assertEqual(get_resp.status_code, 200)

        post_resp = self.client.post(reverse('edit_profile'), {
            'bio': 'Updated bio',
        })
        self.assertEqual(post_resp.status_code, 302)
        self.profile1.refresh_from_db()
        self.assertEqual(self.profile1.bio, 'Updated bio')












from django.test import TestCase, Client
from django.urls import reverse
from fb.models import CustomUser, UserProfile, CreatePost, Comment, FriendRequest, Follow
from django.core.files.uploadedfile import SimpleUploadedFile


class SocialMediaViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = CustomUser.objects.create_user(phone_number='111', password='pass')
        self.user2 = CustomUser.objects.create_user(phone_number='222', password='pass')
        self.user1_profile = UserProfile.objects.create(user=self.user1)
        self.user2_profile = UserProfile.objects.create(user=self.user2)
        self.login_url = reverse('login')
        self.home_url = reverse('home')
        self.client.login(phone_number='111', password='pass')

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
            'firstname': 'Test',
            'lastname': 'User',
            'email': 'test@example.com',
            'phone_number': '333',
            'password': 'pass',
            'Date_of_birth': '2000-01-01'
        })
        self.assertEqual(response.status_code, 200 or 302)

    def test_login_view(self):
        self.client.logout()
        response = self.client.post(self.login_url, {'phone_number': '111', 'password': 'pass'})
        self.assertEqual(response.status_code, 302)

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
        response = self.client.post(reverse('like', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user1, post.likes.all())

    def test_comment_view(self):
        post = CreatePost.objects.create(user=self.user2_profile, content='Post')
        response = self.client.post(reverse('comment', args=[post.id]), {
            'content': 'Nice post!'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(content='Nice post!').exists())

    def test_send_friend_request(self):
        url = reverse('send_request', args=[self.user2.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())

    def test_accept_friend_request(self):
        friend_request = FriendRequest.objects.create(from_user=self.user2, to_user=self.user1)
        url = reverse('accept_request', args=[friend_request.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(FriendRequest.objects.filter(id=friend_request.id).exists())
        self.assertTrue(Follow.objects.filter(follower=self.user1, followed=self.user2).exists())

    def test_show_friend_requests(self):
        url = reverse('show_request', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'send_request.html')

    def test_followers_list(self):
        Follow.objects.create(follower=self.user2, followed=self.user1)
        url = reverse('followers', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user2, response.context['followers'])

    def test_following_list(self):
        Follow.objects.create(follower=self.user1, followed=self.user2)
        url = reverse('following', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user2, response.context['following'])

    def test_edit_profile(self):
        url = reverse('edit_profile')
        response = self.client.post(url, {'bio': 'Updated bio'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserProfile.objects.get(user=self.user1).bio, 'Updated bio')

    def test_user_posts(self):
        CreatePost.objects.create(user=self.user1_profile, content='User post')
        response = self.client.get(reverse('user_posts'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_posts.html')

    def test_delete_post(self):
        post = CreatePost.objects.create(user=self.user1_profile, content='To be deleted')
        response = self.client.post(reverse('delete_post', args=[post.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(CreatePost.objects.filter(id=post.id).exists())

    def test_show_comment_page(self):
        post = CreatePost.objects.create(user=self.user1_profile, content='Comment here')
        response = self.client.get(reverse('show_comments', args=[post.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'morecomment.html')

    def test_post_comment_from_show_page(self):
        post = CreatePost.objects.create(user=self.user1_profile, content='Comment here')
        response = self.client.post(reverse('show_comments', args=[post.id]), {
            'content': 'Another comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content='Another comment').exists())

