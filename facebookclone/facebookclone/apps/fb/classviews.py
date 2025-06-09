from django.shortcuts import render,redirect
from django.views import View
from django.http.response import HttpResponse,HttpResponseRedirect
from django.http import HttpResponse, HttpResponseBadRequest
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
from .models import Comment,FriendRequest
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


class SignUp(View):
    def get(self,request):
        form=forms.SignupForm()
        return render(request, 'fb/signup.html',{'form': form})
    def post(self,request):
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



class Login(View):
    def get(self,request):
        form = forms.LoginForm()
        return render(request, 'fb/login.html', {'form': form})
    
       
    def post(self,request):
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


class LogOut(View):
    def get(self, request):
        logout(request)
        return redirect('login')


class HomePage(View):
    def get(self, request):
        posts = CreatePost.objects.all().order_by('-created_at')
        users = CustomUser.objects.exclude(id=request.user.id)
        return render(request, 'home.html', {
            'posts': posts,
            'users': users,
        })

    def post(self, request):
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if content or image:
            CreatePost.objects.get_or_create(
                user=request.user.userprofile,
                content=content,
                image=image
            )
            return redirect('home')
        
        # If no content or image was provided
        return HttpResponseBadRequest("Content or image required.")



class Post(View):
	def get(self,request):
		return redirect('home')


class Profile(View):
	def post(self,request,user_id):
		target_user = get_object_or_404(CustomUser, id=user_id)
		try:
			user_profile = UserProfile.objects.get(user=target_user)
		except UserProfile.DoesNotExist:
			user_profile = None
		is_following = request.user.following.filter(followed=target_user).exists()
		are_friends = (request.user.following.filter(followed=target_user).exists() and target_user.following.filter(followed=request.user).exists())
		followers_count = target_user.followers.count
		following_count=target_user.following.count
		followers = [f.follower for f in target_user.followers.all()]
		following = [f.followed for f in target_user.following.all()]
		users = CustomUser.objects.exclude(id=request.user.id)
		context = {'target_user': target_user,'user_profile': user_profile,'is_following': is_following,'are_friends': are_friends,'followers_count': followers_count,'following_count': following_count,'followers': followers, 'following': following,'users': users,}
		return render(request, 'fb/profile.html', context)



class EditProfile(View):
	def get(self,request):
		profile,created = UserProfile.objects.get_or_create(user=request.user)
		form = EditProfileForm(instance=profile)
		return render(request, 'edit_profile.html', {'form': form})

	def post(self,request):
		if 'remove_picture' in request.POST:
			profile.profile_picture.delete(save=True)
			return redirect('profile', user_id=request.user.id)
		form = EditProfileForm(request.POST, request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('profile', user_id=request.user.id)

class LikePost(View):
	def post(self, request, post_id):
		post = get_object_or_404(CreatePost, id=post_id)
		user=request.user
		if post.likes.filter(id=user.id).exists(): 
			post.likes.remove(user)
			liked = False
		else:
			post.likes.add(user)
			liked = True
		return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})


class CommentView(View):
	def get(self,request,post_id):
		post = get_object_or_404(CreatePost, pk=post_id)
		latest_comments = post.comments.order_by('-created_at')[:5]
		return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

	def post(self,request,post_id):
		form = CommentForm(request.POST)
		parent_id = request.POST.get('parent_id')
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = request.user
			if parent_id:
				parent_comment = get_object_or_404(Comment,id=parent_id)
				comment.parent = parent_comment
				comment.save()
				if request.headers.get('x-requested-with') == 'XMLHttpRequest':
					html = render_to_string('fb/comment_single.html', {'comment': comment}, request=request)
					return JsonResponse({'success': True, 'comment_html': html})
				return redirect('home')        







class SendFriendRequest(View):
	def post(self,request,user_id):
		to_user = get_object_or_404(CustomUser, id=user_id)
		if request.user != to_user and not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
			FriendRequest.objects.create(from_user=request.user, to_user=to_user)
		return redirect(request.META.get('HTTP_REFERER', '/'))



      

class ShowFriendRequest(View):
	def get(self,request,user_id):
		target_user = get_object_or_404(CustomUser, id=user_id)
		users = CustomUser.objects.exclude(id=request.user.id) 
		sent_requests = FriendRequest.objects.filter(from_user=request.user)
		received_requests = FriendRequest.objects.filter(to_user=request.user)
		following=Follow.objects.filter(follower=request.user).values_list('followed_id',flat=True)
		users=users.exclude(id__in=following)
		sent_request_ids = set(sent_requests.values_list('to_user_id', flat=True))
		received_request_dict = {fr.from_user.id: fr.id for fr in received_requests}
		context={'users': users,'sent_request_ids': sent_request_ids,'received_request_dict': received_request_dict,'target_user':target_user}
		return render(request,'send_request.html',context)


class ShowComments(View):
	def get(self,request,post_id):
		post = get_object_or_404(CreatePost, pk=post_id)
		form = CommentForm()
		return render(request, 'morecomment.html', {'post': post,'form': form,})
	def post(self,request,post_id):
		form = CommentForm(request.POST,request.FILES)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.latest_comments=latest_comments
			new_comment.user = request.user
			new_comment.save()
			return redirect('home')


    









