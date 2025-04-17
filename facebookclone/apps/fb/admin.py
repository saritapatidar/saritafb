from django.contrib import admin

from .models import CustomUser
from .models import UserProfile
from .models import CreatePost
from .models import Friend_request
@admin.register(CustomUser)
class users(admin.ModelAdmin):
    list_display=('firstname','lastname','Date_of_birth','gender','email','phone_number')

# admin.site.register(UserProfile)
@admin.register(UserProfile)


class Postes(admin.ModelAdmin):
    list_display=('content','image')

admin.site.register(CreatePost,Postes)

class FriendRequested(admin.ModelAdmin):
    list_display=('userfrom','to_user')

admin.site.register(FriendRequest,FriendRequested)

