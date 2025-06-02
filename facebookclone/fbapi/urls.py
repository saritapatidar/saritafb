from rest_framework.routers import DefaultRouter
from fbapi import views
from django.urls import path,include
from fbapi.views import Login, LogoutAPI,UserRegistrationView
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


router=DefaultRouter()

router.register('userapi',views.usermodelviewset,basename='user')
router.register('postapi',views.postmodelviewset,basename='post')
router.register('comment',views.commentmodelviewset,basename='comment')

urlpatterns = [

                path('api',include(router.urls)),
                path('api-auth/',include('rest_framework.urls')),
                path('register/', UserRegistrationView.as_view(), name='register'),
    
                path('api/login/',Login.as_view(),name="login"),
                path('logout',LogoutAPI.as_view(),name="logout"),
                # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                
            ]

       