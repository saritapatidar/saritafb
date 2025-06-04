from django.shortcuts import render
from.custompermissions import IsOwnerOrReadOnly
# from .custompermissions import postconditions
# from rest_framework.authentication import TokenAuthentication
from .serializers import userserializer
from .serializers import postserializer
from .serializers import commentserializer,Loginserializer,likeserializer
from rest_framework import viewsets
from .models import CustomUser
from .models import CreatePost
from .models import Comment,Like
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView

# class usermodelviewset(viewsets.ModelViewSet):

# class usermodelviewset(RetrieveUpdateDestroyAPIView):
class usermodelviewset(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = userserializer
    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    permission_classes = [IsOwnerOrReadOnly]


class postmodelviewset(viewsets.ModelViewSet):
    queryset = CreatePost.objects.all()
    serializer_class = postserializer
   
    permission_classes = [IsOwnerOrReadOnly]


    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)  
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

    def get_like_count(self,obj):
    	return getattr(obj,'like_count',obj.likes.count())


class commentmodelviewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = commentserializer
    
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self,serializer):
    	serializer.save(user=self.request.user)

class likemodelviewset(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = likeserializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        post = serializer.validated_data['post']
        user = self.request.user

        # Prevent duplicate likes
        if Like.objects.filter(liked_by=user, post=post).exists():
            raise serializers.ValidationError("You have already liked this post.")

        like= serializer.save()
        like.liked_by.add(user)


class UserRegistrationView(CreateAPIView):

    serializer_class = registrationserializer
    
    permission_classes = [AllowAny]

    
class Login(GenericAPIView):
    serializer_class = Loginserializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            
            user = authenticate(phone_number=phone_number, password=password)

            if user:
                
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': True,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user_id': user.id,
                    'firstname': user.firstname,
                    'phone_number': user.phone_number
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'status': False,
                    'message': 'Invalid phone number or password'
                }, status=status.HTTP_401_UNAUTHORIZED)

        return Response({
            'status': False,
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            # import pdb;pdb.set_trace()
            refresh_token = request.data.get("refresh")

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_400_BAD_REQUEST)






# class likemodelviewset(viewsets.ModelViewSet):
#   queryset=Like.objects.all()
#   serializer_class=likeserializer
#   authentication_classes=[SessionAuthentication,TokenAuthentication]
#   permission_classes=[IsOwnerOrReadOnly]
#   def get_like_count(self,obj):
#       return getattr(obj,'like_count',obj.likes.count())








