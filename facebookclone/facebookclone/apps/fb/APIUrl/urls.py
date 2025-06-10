from rest_framework.routers import DefaultRouter
from fb.APIViews.views import Usermodelviewset,UsermodelviewsetRUD
from django.urls import path,include
from fb.APIViews.views import Login, LogoutAPI,UserRegistrationView
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from fb.APIViews import views

router=DefaultRouter()

# router.register('userapi',Apiviews.usermodelviewset,basename='user')
router.register('postapi',views.Postmodelviewset,basename='post')
router.register('commentapi',views.Commentmodelviewset,basename='comment')
# router.register('parent',views.parentmodelviewset,basename='parent')

urlpatterns = [

                path('',include(router.urls)),
                path('api-auth/',include('rest_framework.urls')),
                path('userapi/',Usermodelviewset.as_view(),name='userapi'),
                path('userapi/<int:pk>/',UsermodelviewsetRUD.as_view(),name='userapi'),
                path('registration/', UserRegistrationView.as_view(), name='registration'),
                path('loginapi/', Login.as_view(), name='loginapi'),
                path('logoutapi/', LogoutAPI.as_view(), name='logoutapi'),
                path('gettoken/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                path('verifytoken/',TokenVerifyView.as_view(),name='token_verify')
                
            ]

       
      
    