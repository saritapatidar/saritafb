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
 
