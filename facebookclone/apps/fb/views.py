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
        return render(request,'home.html')


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
            user = form.save(commit=False)  
            user.password = password  
            user.save()  
            # login(request, user) 
            # return redirect('login_page')  
    
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
        form = ProfileForm()
    return render(request, 'profile.html', {'profile': form})


def post_page(request):
    form = forms.post()
    if request.method == "POST":
        form = forms.post(request.POST,request.FILES)
        if form.is_valid():
            post = forms.save()
            post.user = request.user
            post.save()
            return redirect("home")
    else:
        form = forms.post()

    return render(request,'post.html',{'post':form})

















def login_page(request):
         if request.method == 'POST':
             form = LoginForm(request.POST)
             if form.is_valid():
                 phone_number = form.cleaned_data['phone_number']
                 password = form.cleaned_data['password']
                 user =authenticate(phone_number=phone_number,password=password)
                 if user is not None:
                     login(request, user)
                     return redirect('home') 
                #  else:
                #      form.add_error(None, "Invalid credentials")
         else:
             form = LoginForm()
         return render(request, 'login.html', {'form': form})
