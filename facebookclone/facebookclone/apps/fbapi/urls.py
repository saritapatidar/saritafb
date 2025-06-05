from rest_framework.routers import DefaultRouter
from fbapi import views
from django.urls import path,include
from fbapi.views import Login, LogoutAPI,UserRegistrationView
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


router=DefaultRouter()

router.register('userapi',views.usermodelviewset,basename='user')
router.register('postapi',views.postmodelviewset,basename='post')
router.register('comment',views.commentmodelviewset,basename='comment')
router.register('like',views.likemodelviewset,basename='like')

urlpatterns = [

                path('',include(router.urls)),
                # path('userapi/',views.usermodelviewset.as_view(),name='user'),

                path('api-auth/',include('rest_framework.urls')),
                path('registeration/', UserRegistrationView.as_view(), name='registeration'),
                path('loginapi/', Login.as_view(), name='loginapi'),
                path('logoutapi/', LogoutAPI.as_view(), name='logoutapi'),
                path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('verifytoken/',TokenVerifyView.as_view(),name='token_verify')
                
            ]

       
      
    