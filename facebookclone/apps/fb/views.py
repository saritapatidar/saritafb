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
from .forms import comments
from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import never_cache
from.models import Follow
from .forms import friends
from .forms import EditProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FriendRequest, Follow

# . refers to the current package or current directory where the views.py file is located.


@login_required
@never_cache
def home_page(request):
    posts = CreatePost.objects.all().order_by('-created_at')
    users = CustomUser.objects.exclude(id=request.user.id)
    friend_requests = FriendRequest.objects.filter(to_user=request.user)

    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            CreatePost.objects.create(user=request.user.userprofile,content=content, image=image)

        return redirect('home')

    return render(
        request,
        'home.html',
        {
            'posts': posts,
            'users': users,
            'friend_requests': friend_requests
        }
    )


def logout_user(request):

    logout(request)
    return redirect('login')


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        
        if form.is_valid():
            password = make_password(form.cleaned_data['password'])
            user = form.save()
            user.password = password  
            user.save()  
            return redirect('login')
    
    return render(request, 'signup.html',{'form': form})


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


def profile_page(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)

    try:
        user_profile = UserProfile.objects.get(user=target_user)
    except UserProfile.DoesNotExist:
        user_profile = None

    is_following = request.user.following.filter(followed=target_user).exists()
    users = CustomUser.objects.exclude(id=request.user.id) 
    has_pending_request = FriendRequest.objects.filter(from_user=request.user, to_user=target_user).exists()
    request_from_target = FriendRequest.objects.filter(from_user=target_user, to_user=request.user).first()

    are_friends = (
        request.user.following.filter(followed=target_user).exists() and 
        target_user.following.filter(followed=request.user).exists()
    )

    followers_count = target_user.followers.count()
    following_count = target_user.following.count()

    context = {
        'target_user': target_user,
        'user_profile': user_profile,
        'is_following': is_following,
        'users':users,
        'has_pending_request': has_pending_request,
        'are_friends': are_friends,
        'followers_count': followers_count,
        'following_count': following_count,
        'request_from_target': request_from_target,  
    }
    return render(request, 'profile.html', context)


def post_page(request):
    return redirect('home')
    

def like_post(request, post_id):
    post = get_object_or_404(CreatePost, id=post_id)
    user = request.user

    if post.likes.filter(id=user.id).exists():
    
        post.likes.remove(user)
    else:
    
        post.likes.add(user)

    return redirect('home')
  

def post_detail(request, post_id):
    post = get_object_or_404(CreatePost, pk=post_id)

    if request.method == 'POST':
        form = comments(request.POST,request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('home')
    else:
        form = comments()

    return render(request, 'home.html', {
        'post': post,
        'form': form,
    })


def follow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    Follow.objects.get_or_create(follower=request.user, followed=target_user)
    return redirect('profile',user_id)

def unfollow_user(request, user_id):
    target_user = get_object_or_404(CustomUser, id=user_id)
    Follow.objects.filter(follower=request.user, followed=target_user).delete()
    return redirect('profile',user_id=user_id)



def send_friend_request(request, user_id):
    to_user = get_object_or_404(CustomUser, id=user_id)
    if request.user != to_user and not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists() and not FriendRequest.objects.filter(from_user=to_user, to_user=request.user).exists():
      friend_request = FriendRequest.objects.create(from_user=request.user, to_user=to_user)
      return redirect('friend.html')
    return redirect('profile', user_id=user_id) # Redirect to the user's profile page

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)

    # Only allow accepting friend requests sent to the current user
    if friend_request.to_user != request.user:
        return redirect('accept.html')  

    # # Create mutual follows
    # Follow.objects.get_or_create(follower=request.user, followed=friend_request.from_user)
    # Follow.objects.get_or_create(follower=friend_request.from_user, followed=request.user)

    # Delete the friend request
    friend_request.delete()

    return redirect('accept',user_id=request.user.id)


# def followers_list(request, user_id):
#     user = get_object_or_404(CustomUser, id=user_id)
#     followers = user.followers.all()  # This retrieves all followers of the target user
#     return render(request, 'followers_list.html', {'followers': followers, 'target_user': user})

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

  
def send_friendrequest(request,user_id):
    if request.method == 'POST':
        form = friends(request.POST)
        if form.is_valid():
            to_user_id = form.cleaned_data['user_id']

            if not str(to_user_id).isdigit():
                return redirect('home') 

            to_user = get_object_or_404(CustomUser, pk=user_id)
            # get_object_or_404=make sure we do not send a request to a non existing user

            if request.user == to_user:
                return redirect('friend.html', username=to_user.firstname)

            friend_request, created = friend_request.objects.get_or_create(userfrom=request.user,user_id=user_id)
            # get_or_create=prevent dublicate request 
            

            return redirect('friend.html', username=to_user.firstname)
    
    return redirect('home')

def friend_requests(request,user_id):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'friend.html', {'friend_requests': friend_requests})

def accept_request(request,request_id):
    friend_request=get_object_or_404(FriendRequest,id=request_id)
    if friend_request.to_user==request.user:
        friend_request.is_accepted=True
        friend_request.save()
    return redirect('friend.html')


def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

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


def upload_profile(request):
    profile=get_object_or_404(UserProfile,user=request.user)

    if request.method=="POST":
        form=ProfileForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile',user_id=request.user_id)
    else:
        form=ProfileForm()
    return render(request,'upload.html',{'form':form})