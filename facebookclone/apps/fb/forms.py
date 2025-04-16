from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm


class LoginForm(forms.Form):
    # import pdb;pdb.set_trace()
    phone_number = forms.CharField(max_length=12)
    password = forms.CharField(max_length=8, widget=forms.PasswordInput)
    # password = forms.CharField(max_length=8)

class SignupForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['firstname','lastname','Date_of_birth','gender','email','password','phone_number']
        Date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','profile_picture']

class post(forms.ModelForm):
    class Meta:
        model = CreatePost
        fields = ['content','image']


class friends(forms.ModelForm):
    class Meta:
        model = Friend_request
        fields =['userfrom','to_user']


class likes(forms.ModelForm):
    class Meta:
        # class Meta is basically the inner class. In Django, the use of the Meta class is simply to provide metadata to the ModelForm or the Model class
        # it use metaclass to automatically generate database table based on that class
        model=like
        fields=['post','likes']


