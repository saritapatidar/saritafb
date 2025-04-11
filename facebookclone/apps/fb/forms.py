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
        fields = ['Firstname','Surname','Date_of_birth','gender','email','password','phone_number']
    Date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1900, 2025)))

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

class post(forms.ModelForm):
    class Meta:
        model = create_post
        fields = ['content','image']


class friends(forms.ModelForm):
    class Meta:
        model = Friend_request
        fields =['userfrom','to_user']


class likes(forms.ModelForm):
    class Meta:
        model=like
        fields=['likes']