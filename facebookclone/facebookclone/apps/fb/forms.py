from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm
from .models import CreatePost



class LoginForm(forms.Form):

    # import pdb;pdb.set_trace()
    phone_number = forms.CharField(max_length=12)
    password = forms.CharField(max_length=8,widget=forms.PasswordInput)
   
    # password = forms.CharField(max_length=8)

class SignupForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['firstname','lastname','Date_of_birth','gender','email','phone_number','password']
        widgets={'Date_of_birth':forms.SelectDateWidget(years=range(1990, 2025)),'password': forms.PasswordInput}

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','profile_picture']

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = CreatePost
        fields = ['user','content','image']


class friends(forms.ModelForm):
    class Meta:
        model = FriendRequest
        fields =['from_user','to_user']


# class likes(forms.ModelForm):
#     class Meta:
#         # class Meta is basically the inner class. In Django, the use of the Meta class is simply to provide metadata to the ModelForm or the Model class
#         # it use metaclass to automatically generate database table based on that class
#         model=Like
#         fields=['post','liked_by']



class commentform(forms.ModelForm):
    class Meta:
        model=comment
        fields=['text']


class FollowForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model=Follow
        unique_together = ('follower','followed')


class EditProfileForm(forms.ModelForm):
        class Meta:
            model = UserProfile
            fields = ('bio','profile_picture') 