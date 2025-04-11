from django.contrib import admin

from .models import CustomUser
from .models import UserProfile
from .models import create_post
from .models import Friend_request

@admin.register(CustomUser)
class users(admin.ModelAdmin):
    list_display=('Firstname','Surname','Date_of_birth','gender','email','phone_number')

admin.site.register(UserProfile)
@admin.register(create_post)
class postes(admin.ModelAdmin):
    list_display=('content','image')

@admin.register(Friend_request)
class friends(admin.ModelAdmin):
    list_display=('userfrom','to_user')
