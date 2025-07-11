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
from rest_framework.response import Response
from .models import UserProfile, CreatePost, CustomUser, Comment, FriendRequest, Follow
from .forms import ProfileForm, LoginForm, CreatePostForm, CommentForm, friends, EditProfileForm, SignupForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from django.core.paginator import Paginator
from django.views.decorators.cache import cache_page
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .tasks import send_birthday_emails
import stripe
from django.conf import settings 

# stripe.api_key = 'sk_test_51Re8H3PYWASMvughug4zD3uRy5q2Qg9CefzagdFPUrLstRFcIJcFK5Rnqmzd6CWL6jZ1ShM9MISvheeb60o4Irbm00etQLg56u'

stripe.api_key=settings.STRIPE_SECRET_KEY

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator
from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)



        



class HomePage(LoginRequiredMixin, View):
    @method_decorator(never_cache)
    def get(self, request):
        logger.info(f"{request.user}")
        
        posts_list = CreatePost.objects.all().order_by('-created_at')
        paginator = Paginator(posts_list, 5)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        logger.debug(f"Total posts: {posts_list.count()}")
        logger.debug(f"Posts on page {page_number}: {page_obj.object_list.count()}")

        users = CustomUser.objects.exclude(id=request.user.id)
        return render(request, 'home.html', {'page_obj': page_obj, 'users': users})

    def post(self, request):
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if content or image:
            logger.info(f"Post created by user {request.user}")
            
          
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            CreatePost.objects.create(user=profile, content=content, image=image)

            # Send notification
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "notifications",
                {
                    "type": "send_notification",
                    "message": f"{request.user.firstname} created a new post!"
                }
            )
        else:
            logger.warning(f"Empty post attempt by user {request.user}")

        posts_list = CreatePost.objects.all().order_by('-created_at')
        paginator = Paginator(posts_list, 5)

        page_number = request.GET.get('page') or 1
        page_obj = paginator.get_page(page_number)
        users = CustomUser.objects.exclude(id=request.user.id)

        return render(request, 'home.html', {'page_obj': page_obj, 'users': users})



class Signup(View):
    def get(self,request):
        form = SignupForm()
        logger.info('signup form is ')
        return render(request, 'fb/signup.html', {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            logger.info("signup form is valid")
            user = form.save()
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            email=user.email
            # subject="Test Email"
            # message="Accound is created"
            # from_email="saritapatidar@thoughtwin.com"
            # recipient_list=[email]
            send_mail("Test Email",
                      "Accound is created",
                      "saritapatidar@thoughtwin.com",
                       [email])
            # send_email_task.delay(subject, message, from_email, recipient_list)
            # send_birthday_reminder.delay(subject, message, 'saritapatidar@thoughtwin.com', [user.email])
            send_birthday_emails.delay()
            return redirect('login')
        else:
            logger.warning("signup form is not valid")
        return render(request, 'fb/signup.html', {'form': form})

      
class Login(View):
    def get(self, request):
        form = LoginForm()
        logger.info('login form ')
        return render(request, 'fb/login.html', {'form': form})
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            logger.info('login form is valid')
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are logged in!')
                return redirect('home')
            form.add_error(None, "Invalid")
        return render(request, 'fb/login.html', {'form': form})

class Logout(View):
    def get(self, request):
        logger.info(f"User {request.user} logged out.")
        logout(request)
        return redirect('login')


class Post(RedirectView):
    url = reverse_lazy('home')


class Profile(LoginRequiredMixin, View):
    def get(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        logger.info(f"{request.user} is viewing profile of {target_user}")
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
        # import pdb;pdb.set_trace()
        user = request.user

        liked =not post.likes.filter(id=user.id).exists()

        if liked:
            logger.info(f"{user} liked post {post_id}")
            post.likes.add(user)
        else:
            logger.info(f"{user} unliked post {post_id}")
            post.likes.remove(user)
        return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})



class CommentView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(CreatePost, pk=post_id)
        form = CommentForm(request.POST)
        parent_id = request.POST.get('parent_id')
        if form.is_valid():
            logger.info("commentform is valid")
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            if parent_id:
                comment.parent = get_object_or_404(Comment, id=parent_id)
            comment.save()
            logger.info("comment is done")
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                html = render_to_string('fb/comment_single.html', {'comment': comment}, request=request)
                return JsonResponse({'success': True, 'comment_html': html})
            return redirect('home')
        logger.warning("invalid request")
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)


class SendFriendRequest(LoginRequiredMixin, View):
    def get(self, request, user_id):
        to_user = get_object_or_404(CustomUser, id=user_id)
        if request.user != to_user and not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
            FriendRequest.objects.create(from_user=request.user, to_user=to_user)
            logger.info(f"{request.user} sent friend request to {to_user}")
        return redirect(request.META.get('HTTP_REFERER', '/'))

        
class CancelFriendRequest(LoginRequiredMixin, View):
    def get(self, request, user_id):
        to_user = get_object_or_404(CustomUser, id=user_id)
        friend_request = FriendRequest.objects.filter(from_user=request.user, to_user=to_user).first()
        if friend_request:
            friend_request.delete()
            logger.info(f"{request.user} cancelled friend request to {to_user}")
        return redirect(request.META.get('HTTP_REFERER', '/'))


class AcceptFriendRequest(LoginRequiredMixin, View):
    def get(self, request, request_id):
        friend_request = get_object_or_404(FriendRequest, id=request_id)
        if friend_request.to_user == request.user:
            Follow.objects.get_or_create(follower=request.user, followed=friend_request.from_user)
            Follow.objects.get_or_create(follower=friend_request.from_user, followed=request.user)
            friend_request.delete()
            logger.info(f"{request.user} accepted friend request from {friend_request.from_user}")
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

@method_decorator(cache_page(60*2),name='get')
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

@method_decorator(cache_page(60*2),name='get')
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
            logger.info(f"{request.user} removed profile picture.")
            profile.profile_picture.delete(save=True)
            return redirect('profile', user_id=request.user.id)
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            logger.info("EditProfileForm is valid")
            form.save()
            return redirect('profile', user_id=request.user.id)

        logger.warning("EditProfileForm is not valid")
        return render(request, 'edit_profile.html', {'form': form})

@method_decorator(cache_page(60*2),name='get')
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
        logger.info(f"User {request.user} deleted post with id {post_id}")
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
            logger.info("commentform is valid")
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            logger.info("new_comment is save")
            return redirect('home')
        logger.warning("commentform is not valid")

        return render(request, 'morecomment.html', {
            'post': post,
            'form': form,
        })




class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': 'Premium Badge',
                    },
                    'unit_amount': 19900,  # ₹199
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f'http://localhost:8000/upgrade-success/?user_id={user.id}',
            cancel_url='http://localhost:8000/cancel/',
        )
        return redirect(session.url)




class UpgradeSuccessView(View):
    def get(self, request):
        user_id = request.GET.get("user_id")

        if not user_id:
            return render(request, "error.html", {"message": "Invalid user ID"})

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return render(request, "error.html", {"message": "User not found"})

        user.is_premium = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request,user)

        return render(request, 'success.html', {'user_id': user_id})