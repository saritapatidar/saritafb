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

urlpatterns = [
      path('admin/', admin.site.urls),
      path('signup/',views.signup_page,name='signup'),
      path('login/',views.login_page,name='login'),
      path('logout/',views.logout_user,name='logout'),
      path(' ',views.home_page,name='home'),
      path('profile/',views.profile_page,name='profile'),
      path('post/',views.post_page,name='post'),
      path('friend_request/',views.send_friendrequest,name='friend_request'),
      path('deletepost/<int:post_id>/', views.delete_post, name='delete_post'),
      path('myposts/', views.user_posts, name='user_posts'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
