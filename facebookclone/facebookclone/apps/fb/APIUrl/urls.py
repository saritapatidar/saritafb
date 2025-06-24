from rest_framework.routers import DefaultRouter
from fb.APIViews.views import Usermodelviewset,UsermodelviewsetRUD
from django.urls import path,include
from fb.APIViews.views import Login, LogoutAPI,UserRegistrationView
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from fb.APIViews import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router=DefaultRouter()

# router.register('userapi',Apiviews.usermodelviewset,basename='user')
router.register('postapi',views.Postmodelviewset,basename='post')
router.register('commentapi',views.Commentmodelviewset,basename='comment')
# router.register('parent',views.parentmodelviewset,basename='parent')
schema_view = get_schema_view(
    openapi.Info(
        title="FB Clone API",
        default_version='v1',
        description="API documentation for your Django FB clone project",
        contact=openapi.Contact(email="saritapatidar@thoughtwin.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

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
                path('verifytoken/',TokenVerifyView.as_view(),name='token_verify'),
                path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
                
            ]

       
      
    