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
from pathlib import Path
from .models import CreatePost
from .models import CustomUser
from django.shortcuts import get_object_or_404
from . import forms
from .forms import LoginForm
from .forms import CreatePostForm
# from .forms import Like
from .forms import commentform
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import never_cache
from.models import Follow
from .forms import friends
from .forms import EditProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, Follow
from django.core.mail import send_mail

# . refers to the current package or current directory where the views.py file is located.


@login_required
@never_cache
def home_page(request):
    posts = CreatePost.objects.all().order_by('-created_at')
    users = CustomUser.objects.exclude(id=request.user.id)
    # friend_requests = FriendRequest.objects.filter(to_user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            CreatePost.objects.get_or_create(user=request.user.userprofile,content=content, image=image)

        return redirect('home')
     # All users except the current user
    users = CustomUser.objects.exclude(id=request.user.id)

    # Friend requests
    # sent_requests = FriendRequest.objects.filter(from_user=request.user)
    # received_requests = FriendRequest.objects.filter(to_user=request.user)

    # sent_request_ids = set(sent_requests.values_list('to_user_id', flat=True))
    # received_request_dict = {fr.from_user.id: fr.id for fr in received_requests}



    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'users': users,
            'users': users,
            # 'sent_request_ids': sent_request_ids,
            # 'received_request_dict': received_request_dict,
            
        }
    )


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        
        if form.is_valid():
            password = make_password(form.cleaned_data['password'])
            user = form.save()
            user.password = password  
            user.save()
            email=user.email
            send_mail("Test Email",
                      "Accound is created",
                      "saritapatidar@thoughtwin.com",
                       [email])
            return redirect('login')
    return render(request, 'fb/signup.html',{'form': form})


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
                form.add_error(None, "Invalid") 
    
    else:
        form = forms.LoginForm()
    
    return render(request, 'fb/login.html', {'form': form})


def logout_user(request):

    logout(request)
    return redirect('login')


def profile_page(request,user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    try:
        user_profile = UserProfile.objects.get(user=target_user)
    except UserProfile.DoesNotExist:
        user_profile = None

    # Check if the current user is following the target user
    is_following = request.user.following.filter(followed=target_user).exists()

    # Check if they are mutual friends (following each other)
    are_friends = (
        request.user.following.filter(followed=target_user).exists() and 
        target_user.following.filter(followed=request.user).exists()
    )

    # Followers & Following counts
    followers_count = target_user.followers.count
    following_count=target_user.following.count
    # Extract CustomUser objects from Follow relations
    followers = [f.follower for f in target_user.followers.all()]
    following = [f.followed for f in target_user.following.all()]

    # All users except the current user
    users = CustomUser.objects.exclude(id=request.user.id)


    context = {
        'target_user': target_user,
        'user_profile': user_profile,
        'is_following': is_following,
        'are_friends': are_friends,
        'followers_count': followers_count,
        'following_count': following_count,
        'followers': followers,  # List of CustomUser followers
        'following': following,  # List of CustomUser following
        'users': users,
       }
    return render(request, 'fb/profile.html', context)


def post_page(request):
    return redirect('home')
    

def like_post(request, post_id):
    post = get_object_or_404(CreatePost, id=post_id)
    user = request.user

    if post.likes.filter(id=user.id).exists():
    
        post.likes.remove(user)
    else:
    
        post.likes.add(user)
    # return render(request,'likes.html')

    return redirect('home')
  

def comments(request, post_id):
    post = get_object_or_404(CreatePost, pk=post_id)

    if request.method == 'POST':
        form = commentform(request.POST,request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('home')
    else:
        form = commentform()

    return render(request, 'home.html', {
        'post': post,
        'form': form,
    })

def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)

    if request.user != to_user and not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)

    return redirect(request.META.get('HTTP_REFERER', '/'))

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    if friend_request.to_user == request.user:
        Follow.objects.get_or_create(follower=request.user, followed=friend_request.from_user)
        Follow.objects.get_or_create(follower=friend_request.from_user, followed=request.user)
        friend_request.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))

def show_friend_request(request,user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    users = CustomUser.objects.exclude(id=request.user.id)

    # Friend requests
    sent_requests = FriendRequest.objects.filter(from_user=request.user)
    received_requests = FriendRequest.objects.filter(to_user=request.user)

    sent_request_ids = set(sent_requests.values_list('to_user_id', flat=True))
    received_request_dict = {fr.from_user.id: fr.id for fr in received_requests}

    context={'users': users,
        'sent_request_ids': sent_request_ids,
        'received_request_dict': received_request_dict,
        'target_user':target_user
    }
    return render(request,'send_request.html',context)




def followers_list(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    follower_relations = Follow.objects.filter(followed=user)
    followers = [rel.follower for rel in follower_relations]

    # List of users that the current user is following
    current_user_following = [rel.followed for rel in Follow.objects.filter(follower=request.user)]

    return render(request, 'followers_list.html', {
        'followers': followers,
        'target_user': user,
        'current_user_following': current_user_following
    })



def following_list(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    following_relations = Follow.objects.filter(follower=user)
    following = [relation.followed for relation in following_relations]
    return render(request, 'following_list.html', {'following': following, 'target_user': user})

# get_object_or_404 is used in Django to retrieve a single object from the database, 
# and if the object does not exist, it automatically raises an Http404 exception,
    
# get_or_create() in Django serves as a convenient method for retrieving an 
# object from the database or creating it if it doesn't exist.
 



def edit_profile(request):
    profile,created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'remove_picture' in request.POST:
            profile.profile_picture.delete(save=True)
            return redirect('profile', user_id=request.user.id)

        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})


# def follow_user(request, user_id):
#     target_user = get_object_or_404(CustomUser, id=user_id)
#     Follow.objects.get_or_create(follower=request.user, followed=target_user)
#     return redirect('profile',user_id)

# def unfollow_user(request, user_id):
#     target_user = get_object_or_404(CustomUser, id=user_id)
#     Follow.objects.filter(follower=request.user, followed=target_user).delete()
#     return redirect('profile',user_id=user_id)

