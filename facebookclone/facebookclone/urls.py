"""
URL configuration for facebookclone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from apps.fb import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
      path('admin/', admin.site.urls),
      path('signup/',views.signup_page,name='signup'),
      path('',views.login_page,name='login'),
      path('logout/',views.logout_user,name='logout'),
      path(' ',views.home_page,name='home'),
      path('profile/<int:user_id>/',views.profile_page,name='profile'),
      path('post/',views.post_page,name='post'),
      path('friendrequest/<int:user_id>/',views.send_friendrequest,name='friendrequest'),
      path('acceptrequest/',views.accept_request,name='acceptrequest'),
      
      path('like/<int:post_id>/', views.like_post, name='likepost'),
      path('commen/<int:post_id>/',views.post_detail,name='commen'),
      path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
      path('unfollow/<int:user_id>/',views.unfollow_user, name='unfollow_user'),
      path('password_reset/',auth_views.PasswordResetView.as_view(),name="password_reset"),
      path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
      path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
      path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
      path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
      path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
     
      path('profile/<int:user_id>/followers/', views.followers_list, name='followers_list'),
      path('profile/<int:user_id>/following/', views.following_list, name='following_list'),
    
      path('profile/edit/', views.edit_profile, name='edit_profiles'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# like/<int:post_id>/ defines a URL structure that captures an integer value from the URL and assigns 
# it to the variable post_id. This pattern is commonly used to handle requests related to specific posts, 
# where post_id represents the unique identifier of a post.