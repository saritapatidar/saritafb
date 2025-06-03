from django.shortcuts import render
from.custompermissions import IsOwnerOrReadOnly
# from .custompermissions import postconditions
# from rest_framework.authentication import TokenAuthentication
from .serializers import userserializer
from .serializers import postserializer
from .serializers import commentserializer,Loginserializer,likeserializer
from rest_framework import viewsets
from .models import CustomUser
from .models import CreatePost,Like
from .models import comment
from rest_framework.authentication import BasicAuthentication,SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView
from .serializers import Loginserializer, registrationserializer
from rest_framework_simplejwt.authentication import JWTAuthentication


class usermodelviewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = userserializer
    authentication_classes = [SessionAuthentication,TokenAuthentication,JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]


class postmodelviewset(viewsets.ModelViewSet):
    queryset = CreatePost.objects.all()
    serializer_class = postserializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

    # def get_like_count(self,obj):
    # 	return getattr(obj,'like_count',obj.likes.count())


class commentmodelviewset(viewsets.ModelViewSet):
    queryset = comment.objects.all()
    serializer_class = commentserializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self,serializer):
    	serializer.save(user=self.request.user)

class likemodelviewset(viewsets.ModelViewSet):
	queryset=Like.objects.all()
	serializer_class=likeserializer
	authentication_classes=[SessionAuthentication,TokenAuthentication]
	permission_classes=[IsOwnerOrReadOnly]
	def get_like_count(self,obj):
		return getattr(obj,'like_count',obj.likes.count())



class UserRegistrationView(CreateAPIView):
    serializer_class = registrationserializer
    permission_classes = [AllowAny]


class Login(GenericAPIView):
    serializer_class = Loginserializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            user = authenticate(request, username=phone_number, password=password)

            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    "status": True,
                    "token": str(token),
                    "message": "Login successful"
                })
            else:
                return Response({
                    "status": False,
                    "message": "Invalid phone number or password"
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            "status": False,
            "errors": serializer.errors,
            "message": "Validation failed"
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
		





