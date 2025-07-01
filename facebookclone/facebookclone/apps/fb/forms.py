from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm
from .models import CreatePost



class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=12)
    password = forms.CharField(max_length=8,widget=forms.PasswordInput)
   
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



        # class Meta is basically the inner class. In Django, the use of the Meta class is simply to provide metadata to the ModelForm or the Model class
        # it use metaclass to automatically generate database table based on that class
       
        
class FollowForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    class Meta:
        model=Follow
        unique_together = ('follower','followed')


class EditProfileForm(forms.ModelForm):
        class Meta:
            model = UserProfile
            fields = ('bio','profile_picture')



# class EditProfileForm(forms.ModelForm):
#     first_name = forms.CharField(required=False)
#     last_name = forms.CharField(required=False)
#     date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
#     phone_number = models.CharField(max_length=12,unique=True,null=True)


#     class Meta:
#         model = UserProfile
#         fields = ['bio', 'profile_picture']

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if self.user:
#             self.fields['first_name'].initial = self.user.firstname
#             self.fields['last_name'].initial = self.user.lastname
#             self.fields['date_of_birth'].initial = self.user.Date_of_birth
            

#     def save(self, commit=True):
#         profile = super().save(commit=False)
#         if commit:
#             profile.save()
#             self.user.firstname = self.cleaned_data['first_name']
#             self.user.lastname = self.cleaned_data['last_name']
#             self.user.Date_of_birth = self.cleaned_data['date_of_birth']
            
#             self.user.save()
#         return profile



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
