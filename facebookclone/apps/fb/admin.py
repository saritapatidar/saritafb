from django.contrib import admin

from .models import CustomUser
from .models import UserProfile
from .models import CreatePost
from .models import Friend_request
@admin.register(CustomUser)
class users(admin.ModelAdmin):
    list_display=('firstname','lastname','Date_of_birth','gender','email','phone_number')

# admin.site.register(UserProfile)

admin.site.register(UserProfile)


class postes(admin.ModelAdmin):
    list_display=('content','image')

admin.register(CreatePost,postes)

class friend_requested(admin.ModelAdmin):
    list_display=('userfrom','to_user')

admin.register(Friend_request,friend_requested)

