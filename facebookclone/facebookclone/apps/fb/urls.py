from django.contrib import admin
from django.urls import path,include
# from fb import views
from fb import classviews
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from .classviews import Signup,Login,Logout,HomePage,Post,LikeView,SendFriendRequest,CommentView,ShowFriendRequest
from .classviews import Profile,ShowComment,AcceptFriendRequest,EditProfileView,DeletePost,UserPost,FollowersList,FollowingListView



urlpatterns = [
      path('signup/',Signup.as_view(),name='signup'),
      path('',Login.as_view(),name='login'),
      path('logout/',Logout.as_view(),name='logout'),
      path(' ',HomePage.as_view(),name='home'),
      path('post/',Post.as_view(),name='post'),
      path('profile/<int:user_id>/',Profile.as_view(),name='profile'),
      path('likepost/<int:post_id>/',LikeView.as_view(), name='likepost'),
      path('commen/<int:post_id>/',CommentView.as_view(),name='commen'),
      path('send_friend_request/<int:user_id>/',SendFriendRequest.as_view(),name='send_friend_request'),
      path('accept_friend_request/<int:request_id>/',AcceptFriendRequest.as_view() ,name='accept_friend_request'), 
      path('show_friends/<int:user_id>/',ShowFriendRequest.as_view(),name='show_friends'),
      path('followers_list/<int:user_id>/',FollowersList.as_view(),name='followers_list'),
      path('following_list/<int:user_id>/',FollowingListView.as_view(),name='following_list'),
      path('profile/edit/',EditProfileView.as_view(),name='edit_profiles'),
      path('morecomment/<int:post_id>/',ShowComment.as_view(),name='morecomment'),
      path('deletepost/<int:post_id>/',DeletePost.as_view(), name='delete_post'),
      path('myposts/',UserPost.as_view(), name='user_posts'),
      path('api/',include('fb.APIUrl.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




      
      # path('signup/',views.signup_page,name='signup'),
      # path('',views.login_page,name='login'),
      # path('logout/',views.logout_user,name='logout'),
      # path(' ',views.home_page,name='home'),
      # path('profile/<int:user_id>/',views.profile_page,name='profile'),
      # path('post/',views.post_page,name='post'),
      # path('likepost/<int:post_id>/', views.like_post, name='likepost'),
      # path('commen/<int:post_id>/',views.comment_view,name='commen'),
      # path('morecomment/<int:post_id>/',views.showcomments,name='morecomment'),
      # path('send_friend_request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
      # path('accept_friend_request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'), 
      # path('profile/edit/',views.edit_profile,name='edit_profiles'),
      # path('show_friends/<int:user_id>/',views.show_friend_request,name='show_friends'),
      # path('deletepost/<int:post_id>/', views.delete_post, name='delete_post'),
      # path('myposts/', views.user_posts, name='user_posts'),
      # path('api/',include('fb.Fbapi.Apiurls')),

    
   
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# like/<int:post_id>/ defines a URL structure that captures an integer value from the URL and assigns 
# it to the variable post_id. This pattern is commonly used to handle requests related to specific posts, 
# where post_id represents the unique identifier of a post.