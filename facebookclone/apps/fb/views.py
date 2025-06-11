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

from rest_framework.authentication import TokenAuthentication, SessionAuthentication

# from rest_framework.authentication import BasicAuthentication
class usermodelviewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = userserializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]


class postmodelviewset(viewsets.ModelViewSet):
    queryset = CreatePost.objects.all()
    serializer_class = postserializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class commentmodelviewset(viewsets.ModelViewSet):
    queryset = comment.objects.all()
    serializer_class = commentserializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework import status
from .serializers import Loginserializer, registrationserializer
from rest_framework.permissions import AllowAny
from rest_framework.generics import CreateAPIView
from .models import CustomUser
from rest_framework.generics import GenericAPIView


class UserRegistrationView(CreateAPIView):
    serializer_class = registrationserializer
    permission_classes = [AllowAny]


class Login(GenericAPIView):
    serializer_class = Loginserializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            user = authenticate(request, username=phone_number, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "status": True,
                    "token": str(token),
                    "message": "Login successful"
                })
            else:
                return Response({
                    "status": False,
                    "message": "Invalid phone number or password"
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            "status": False,
            "errors": serializer.errors,
            "message": "Validation failed"
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


path('api', include(router.urls)),
      path('api-auth/',include('rest_framework.urls')),
      path('register/', UserRegistrationView.as_view(), name='register'),
      path('loginapi/', Login.as_view(), name='loginapi'),
      path('logoutapi/', LogoutAPI.as_view(), name='logoutapi'),
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
.env
# Django Secret Key
SECRET_KEY=django-insecure-##obv#n&=(kuxcgy5)qknuic0a00$7d-3c2+m-$0erq+psash5

# Debug mode
DEBUG=True

# Allowed Hosts
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration
DB_NAME=facebook1
DB_USER=postgres
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=saritapatidar@thoughtwin.com
EMAIL_HOST_PASSWORD=toop flxa aygt fdgu


# def login_page(request):
#          if request.method == 'POST':
#              form = LoginForm(request.POST)
#              if form.is_valid():
#                  phone_number = form.cleaned_data['phone_number']
#                  password = form.cleaned_data['password']
#                  user =authenticate(phone_number=phone_number,password=password)
#                  if user is not None:
#                      login(request, user)
#                      return redirect('home') 
#                 #  else:
#                 #      form.add_error(None, "Invalid credentials")
#          else:
#              form = LoginForm()
#          return render(request, 'login.html', {'form': form})
 
class Login(GenericAPIView):
    serializer_class = Loginserializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            # 📌 Authenticate user using phone number and password
            user = authenticate(phone_number=phone_number, password=password)

            if user:
                # ✅ Generate JWT token (refresh & access)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': True,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'firstname': user.firstname,
                    'phone_number': user.phone_number
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': False,
                    'message': 'Invalid phone number or password'
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'status': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken

class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_400_BAD_REQUEST)
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'BLACKLIST_AFTER_ROTATION': True,
    'ROTATE_REFRESH_TOKENS': True,
}
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt.token_blacklist',
]
class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        user = self.request.user

        # Check if already liked
        if Like.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("You have already liked this post.")

        serializer.save(user=user)
class Comment(models.Model):
    post = models.ForeignKey(CreatePost, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

    class Meta:
        ordering = ['created_at']
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'parent']
        widgets = {'parent': forms.HiddenInput()}  # hide parent field from user
from django.shortcuts import get_object_or_404, redirect, render
from .models import CreatePost, Comment
from .forms import CommentForm

def comments(request, post_id):
    post = get_object_or_404(CreatePost, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('home')
    else:
        form = CommentForm()

    # Pass all comments to template (including replies)
    comments = post.comments.filter(parent__isnull=True)  # only top-level comments

    return render(request, 'home.html', {
        'post': post,
        'form': form,
        'comments': comments,
    })
        comment_single.html
<div class="comment" style="margin-left: {{ level|default:0 }}px;">
    <strong>{{ comment.user.firstname }} {{ comment.user.lastname }}:</strong> {{ comment.text }}<br>
    <small>{{ comment.created_at|date:"d M Y" }} | {{ comment.created_at|timesince }}</small>

    <!-- Reply button triggers showing reply form (optional, can be a link that shows form) -->
    <a href="#" class="reply-link" data-comment-id="{{ comment.id }}">Reply</a>

    <!-- Replies -->
    {% for reply in comment.replies.all %}
        {% include "comment_single.html" with comment=reply level=level|add:"20" %}
    {% endfor %}
</div>
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CreatePost
from .serializers import postserializer

class postmodelviewset(viewsets.ModelViewSet):
    queryset = CreatePost.objects.all()
    serializer_class = postserializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Agar image pass nahi ki gayi to purani image hi rahe
        if not request.data.get('image'):
            request.data._mutable = True
            request.data['image'] = instance.image

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='likes', permission_classes=[IsAuthenticated])
    def like_unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='likes', permission_classes=[IsAuthenticated])
    def liked_posts(self, request):
        user = request.user
        posts = CreatePost.objects.filter(likes=user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






from django.test import TestCase
from django.core.exceptions import ValidationError
from fb.models import CustomUser, UserProfile, CreatePost, Follow, FriendRequest, Comment

class ModelTests(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            phone_number='1234567890',
            email='test@example.com',
            password='Password@123',
            firstname='Test',
            lastname='User'
        )
        self.profile = UserProfile.objects.create(user=self.user)

    def test_user_creation_success(self):
        self.assertEqual(self.user.phone_number, '1234567890')
        self.assertTrue(self.user.check_password('Password@123'))

    def test_phone_number_validation_invalid(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                phone_number='abc123',
                email='fail@example.com',
                password='Password@123'
            )
            user.clean()

    def test_password_validation_too_short(self):
        with self.assertRaises(ValidationError):
            user = CustomUser(
                phone_number='1234567890',
                email='fail@example.com',
                password='Pwd@1'
            )
            user.clean()

    def test_user_profile_created(self):
        self.assertEqual(self.profile.user, self.user)

    def test_create_post(self):
        post = CreatePost.objects.create(user=self.profile, content="My first post")
        self.assertEqual(post.content, "My first post")
        self.assertEqual(post.user, self.profile)

    def test_like_post(self):
        post = CreatePost.objects.create(user=self.profile, content="Like this post")
        post.likes.add(self.user)
        self.assertEqual(post.likes.count(), 1)
        self.assertIn(self.user, post.likes.all())

    def test_follow_user(self):
        user2 = CustomUser.objects.create_user(
            phone_number='9876543210',
            email='other@example.com',
            password='Password@456',
            firstname='Other',
            lastname='User'
        )
        follow = Follow.objects.create(follower=self.user, followed=user2)
        self.assertEqual(follow.follower, self.user)
        self.assertEqual(follow.followed, user2)

    def test_friend_request(self):
        user2 = CustomUser.objects.create_user(
            phone_number='9998887776',
            email='friend@example.com',
            password='Password@456',
            firstname='Friend',
            lastname='Request'
        )
        friend_req = FriendRequest.objects.create(from_user=self.user, to_user=user2)
        self.assertEqual(friend_req.from_user, self.user)
        self.assertEqual(friend_req.to_user, user2)

    def test_comment_and_reply(self):
        post = CreatePost.objects.create(user=self.profile, content="Post with comments")
        comment = Comment.objects.create(post=post, user=self.user, text="Nice post!")
        reply = Comment.objects.create(post=post, user=self.user, parent=comment, text="Thanks!")
        
        self.assertEqual(comment.replies.count(), 1)
        self.assertEqual(comment.replies.first().text, "Thanks!")


