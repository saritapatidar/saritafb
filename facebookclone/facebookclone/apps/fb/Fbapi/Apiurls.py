from rest_framework.routers import DefaultRouter
from .import Apiviews
from django.urls import path,include
from .Apiviews import Login, LogoutAPI,UserRegistrationView
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView


router=DefaultRouter()

router.register('userapi',Apiviews.usermodelviewset,basename='user')
router.register('postapi',Apiviews.postmodelviewset,basename='post')
router.register('commentapi',Apiviews.commentmodelviewset,basename='comment')
# router.register('parent',views.parentmodelviewset,basename='parent')

urlpatterns = [

                path('',include(router.urls)),
                path('api-auth/',include('rest_framework.urls')),
                path('registration/', UserRegistrationView.as_view(), name='registration'),
                path('loginapi/', Login.as_view(), name='loginapi'),
                path('logoutapi/', LogoutAPI.as_view(), name='logoutapi'),
                path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('verifytoken/',TokenVerifyView.as_view(),name='token_verify')
                
            ]

       
      
    