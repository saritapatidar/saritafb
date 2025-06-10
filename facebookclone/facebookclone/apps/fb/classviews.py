from django.shortcuts import render,redirect
from django.views import View
from django.http.response import HttpResponse,HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from .forms import ProfileForm
from django.contrib.auth.hashers import make_password ,check_password
from django.urls import reverse
from pathlib import Path
from django.shortcuts import get_object_or_404
from . import forms
from .forms import LoginForm
from .forms import CreatePostForm
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from.models import Follow
from .forms import friends
from .forms import EditProfileForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Follow
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.views.generic.base import RedirectView
from django.urls import reverse_lazy
from .models import UserProfile, CreatePost, CustomUser, Comment, FriendRequest, Follow
from .forms import ProfileForm, LoginForm, CreatePostForm, CommentForm, friends, EditProfileForm, SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator


class HomePage(LoginRequiredMixin, View):
    @method_decorator(never_cache)
    def get(self, request):
        posts = CreatePost.objects.all().order_by('-created_at')
        users = CustomUser.objects.exclude(id=request.user.id)
        return render(request, 'home.html', {'posts': posts, 'users': users})

    def post(self, request):
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content or image:
            CreatePost.objects.get_or_create(user=request.user.userprofile, content=content, image=image)
        return redirect('home')

class Signup(View):
    def get(self, request):
        form = SignupForm()
        return render(request, 'fb/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            send_mail("Test Email", "Account is created", "saritapatidar@thoughtwin.com", [user.email])
            return redirect('login')
        return render(request, 'fb/signup.html', {'form': form})

class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'fb/login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            form.add_error(None, "Invalid")
        return render(request, 'fb/login.html', {'form': form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class Post(RedirectView):
    url = reverse_lazy('home')


class Profile(LoginRequiredMixin, View):
    def get(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        user_profile = UserProfile.objects.filter(user=target_user).first()
        is_following = request.user.following.filter(followed=target_user).exists()
        are_friends = is_following and target_user.following.filter(followed=request.user).exists()
        followers = [f.follower for f in target_user.followers.all()]
        following = [f.followed for f in target_user.following.all()]
        context = {
            'target_user': target_user,
            'user_profile': user_profile,
            'is_following': is_following,
            'are_friends': are_friends,
            'followers_count': target_user.followers.count(),
            'following_count': target_user.following.count(),
            'followers': followers,
            'following': following,
            'users': CustomUser.objects.exclude(id=request.user.id),
        }
        return render(request, 'fb/profile.html', context)


class LikeView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(CreatePost, id=post_id)
        user = request.user
        liked = not post.likes.filter(id=user.id).exists()
        if liked:
            post.likes.add(user)
        else:
            post.likes.remove(user)
        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})


class CommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(CreatePost, pk=post_id)
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('fb/comment_single.html', {'comment': comment}, request=request)
                return JsonResponse({'success': True, 'comment_html': html})
            return redirect('home')
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


class SendFriendRequest(LoginRequiredMixin, View):
    def get(self, request, user_id):
        to_user = get_object_or_404(CustomUser, id=user_id)
        if request.user != to_user and not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return redirect(request.META.get('HTTP_REFERER', '/'))


class AcceptFriendRequest(LoginRequiredMixin, View):
    def get(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        if friend_request.to_user == request.user:
            Follow.objects.get_or_create(follower=request.user, followed=friend_request.from_user)
            Follow.objects.get_or_create(follower=friend_request.from_user, followed=request.user)
            friend_request.delete()
        return redirect(request.META.get('HTTP_REFERER', '/'))


class ShowFriendRequest(LoginRequiredMixin, View):
    def get(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        users = CustomUser.objects.exclude(id=request.user.id)
        sent_requests = FriendRequest.objects.filter(from_user=request.user)
        received_requests = FriendRequest.objects.filter(to_user=request.user)
        following = Follow.objects.filter(follower=request.user).values_list('followed_id', flat=True)
        users = users.exclude(id__in=following)
        sent_request_ids = set(sent_requests.values_list('to_user_id', flat=True))
        received_request_dict = {fr.from_user.id: fr.id for fr in received_requests}
        context = {
            'users': users,
            'sent_request_ids': sent_request_ids,
            'received_request_dict': received_request_dict,
            'target_user': target_user
        }
        return render(request, 'send_request.html', context)


class FollowersList(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        follower_relations = Follow.objects.filter(followed=user)
        followers = [rel.follower for rel in follower_relations]
        current_user_following = [rel.followed for rel in Follow.objects.filter(follower=request.user)]
        return render(request, 'followers_list.html', {
            'followers': followers,
            'target_user': user,
            'current_user_following': current_user_following
        })


class FollowingListView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        following_relations = Follow.objects.filter(follower=user)
        following = [relation.followed for relation in following_relations]
        return render(request, 'following_list.html', {'following': following, 'target_user': user})


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        form = EditProfileForm(instance=profile)
        return render(request, 'edit_profile.html', {'form': form})

    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if 'remove_picture' in request.POST:
            profile.profile_picture.delete(save=True)
            return redirect('profile', user_id=request.user.id)
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
        return render(request, 'edit_profile.html', {'form': form})


class UserPost(LoginRequiredMixin, View):
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        posts = CreatePost.objects.filter(user=user_profile).order_by('-created_at')
        return render(request, 'user_posts.html', {'posts': posts})


class DeletePost(LoginRequiredMixin, View):
    def get(self, request, post_id):
        user_profile = UserProfile.objects.get(user=request.user)
        post = get_object_or_404(CreatePost, id=post_id, user=user_profile)
        return render(request, 'confirm_delete.html', {'post': post})

    def post(self, request, post_id):
        user_profile = UserProfile.objects.get(user=request.user)
        post = get_object_or_404(CreatePost, id=post_id, user=user_profile)
        post.delete()
        return redirect('user_posts')


class ShowComment(View):
    def get(self, request, post_id):
        post = get_object_or_404(CreatePost, pk=post_id)
        form = CommentForm()
        return render(request, 'morecomment.html', {
            'post': post,
            'form': form,
        })

    def post(self, request, post_id):
        post = get_object_or_404(CreatePost, pk=post_id)
        form = CommentForm(request.POST, request.FILES)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('home')

        return render(request, 'morecomment.html', {
            'post': post,
            'form': form,
        })
