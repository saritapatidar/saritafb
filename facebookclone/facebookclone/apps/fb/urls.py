from django.contrib import admin
from django.urls import path,include
from fb import views
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
# from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token

# router=DefaultRouter()

# router.register('userapi',views.usermodelviewset,basename='user')
# router.register('postapi',views.postmodelviewset,basename='post')
# router.register('comment',views.commentmodelviewset,basename='comment')


urlpatterns = [
      
      path('signup/',views.signup_page,name='signup'),
      path('',views.login_page,name='login'),
      path('logout/',views.logout_user,name='logout'),
      path(' ',views.home_page,name='home'),
      path('profile/<int:user_id>/',views.profile_page,name='profile'),
      path('post/',views.post_page,name='post'),
      path('likepost/<int:post_id>/', views.like_post, name='likepost'),
      path('commen/<int:post_id>/',views.comments,name='commen'),
      path('morecomment/<int:post_id>/',views.showcomments,name='morecomment'),
      path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
      path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'), 
      path('profile/edit/',views.edit_profile,name='edit_profiles'),
      path('show_friends/<int:user_id>/',views.show_friend_request,name='show_friends'),
      path('deletepost/<int:post_id>/', views.delete_post, name='delete_post'),
      path('myposts/', views.user_posts, name='user_posts'),
      path('add_comment/',views.add_comment,name='add_comment')
      
      # path('profile/<int:user_id>/followers/', views.followers_list, name='followers_list'),
      # path('profile/<int:user_id>/following/', views.following_list, name='following_list'),
      # path('api',include(router.urls)),
      # path('api-auth/',include('rest_framework.urls')),

      # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
      
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# like/<int:post_id>/ defines a URL structure that captures an integer value from the URL and assigns 
# it to the variable post_id. This pattern is commonly used to handle requests related to specific posts, 
# where post_id represents the unique identifier of a post.