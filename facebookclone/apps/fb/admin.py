from django.contrib import admin

from .models import CustomUser
from .models import UserProfile
from .models import CreatePost
from .models import FriendRequest
@admin.register(CustomUser)
class users(admin.ModelAdmin):
    list_display=('firstname','lastname','Date_of_birth','gender','email','phone_number')

# admin.site.register(UserProfile)
@admin.register(UserProfile)

@admin.register(CreatePost)
class Postes(admin.ModelAdmin):
    List_display=('user','content','image')

# admin.site.register(CreatePost,Postes)
@admin.register(FriendRequest)
class FriendRequested(admin.ModelAdmin):
    List_display=('userfrom','to_user')

# admin.site.register(FriendRequest,FriendRequested)


