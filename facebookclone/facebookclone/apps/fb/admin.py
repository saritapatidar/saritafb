from django.contrib import admin
from .models import CustomUser
from .models import UserProfile
from .models import CreatePost
from .models import Comment
from .models import Follow

@admin.register(CustomUser)
class users(admin.ModelAdmin):
    list_display=('id','firstname','lastname','Date_of_birth','gender','email','phone_number','is_premium')
    list_display_links=('id','firstname')
    list_filter=('gender',)
    search_fields=('firstname','phone_number')

    actions = ['make_premium']
    def make_premium(self, request, queryset):
        updated = queryset.update(is_premium=True)
        self.message_user(request, f"{updated} user marked as Premium")

    make_premium.short_description = "Mark selected users as Premium"



@admin.register(UserProfile)
class pro(admin.ModelAdmin):
    List_display=('user','bio','profile_picture','following')
    List_display=('user',)
    list_filter=('bio',)
    search_fields=('profile_picture',)

@admin.register(CreatePost)
class Postes(admin.ModelAdmin):
    List_display=('user','content','image')
    List_display=('user',)
    list_filter=('image',)
    



@admin.register(Comment)
class commentes(admin.ModelAdmin):
    List_display=('text')


@admin.register(Follow)
class Follows(admin.ModelAdmin):
    List_display=('follower','followed')
   




# admin.site.register(CreatePost,Postes)
# @admin.register(FriendRequest)
# class FriendRequested(admin.ModelAdmin):
#     List_display=('from_user','to_user')

# admin.site.register(FriendRequest,FriendRequested)
