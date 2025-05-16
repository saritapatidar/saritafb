from django.contrib import admin
from django.urls import path
from fb import views
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView

urlpatterns = [
      
      path('signup/',views.signup_page,name='signup'),
      path('',views.login_page,name='login'),
      path('logout/',views.logout_user,name='logout'),
      path(' ',views.home_page,name='home'),
      path('profile/<int:user_id>/',views.profile_page,name='profile'),
      path('post/',views.post_page,name='post'),
      path('like/<int:post_id>/', views.like_post, name='likepost'),
      path('commen/<int:post_id>/',views.comments,name='commen'),
      # path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
      # path('unfollow/<int:user_id>/',views.unfollow_user, name='unfollow_user'),
      # path('password_reset/',auth_views.PasswordResetView.as_view(),name="password_reset"),
      # path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
      # path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
      # path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
      path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
      path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
      
      path('profile/<int:user_id>/followers/', views.followers_list, name='followers_list'),
      path('profile/<int:user_id>/following/', views.following_list, name='following_list'),
      path('profile/edit/',views.edit_profile,name='edit_profiles'),
      path('show_friends/<int:user_id>/',views.show_friend_request,name='show_friends')
      
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)