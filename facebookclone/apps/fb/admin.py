from django.contrib import admin

from .models import CustomUser
from .models import UserProfile

@admin.register(CustomUser)
class users(admin.ModelAdmin):
    list_display=('Firstname','Surname','Date_of_birth','gender','email','phone_number')

admin.site.register(UserProfile)

