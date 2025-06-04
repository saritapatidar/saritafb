from django.contrib import admin

from .models import CustomUser
from .models import UserProfile
from .models import CreatePost
from .models import FriendRequest
from .models import Comment
from .models import Follow

@admin.register(CustomUser)
class users(admin.ModelAdmin):
    list_display=('firstname','lastname','Date_of_birth','gender','email','phone_number')

# admin.site.register(UserProfile)
@admin.register(UserProfile)
class pro(admin.ModelAdmin):
    List_display=('user','bio','profile_picture','following')

@admin.register(CreatePost)
class Postes(admin.ModelAdmin):
    List_display=('user','content','image')

# admin.site.register(CreatePost,Postes)
@admin.register(FriendRequest)
class FriendRequested(admin.ModelAdmin):
    List_display=('from_user','to_user')

# admin.site.register(FriendRequest,FriendRequested)


@admin.register(Comment)
class commentes(admin.ModelAdmin):
    List_display=('text')


@admin.register(Follow)
class Follows(admin.ModelAdmin):
    List_display=('follower','followed')