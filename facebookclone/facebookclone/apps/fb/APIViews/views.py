from django.shortcuts import render
from fb.custompermissions import IsOwnerOrReadOnly
from fb.serializers import userserializer
from fb.serializers import postserializer
from fb.serializers import commentserializer,Loginserializer
from rest_framework import viewsets
from fb.models import CustomUser
from fb.models import CreatePost
from fb.models import Comment
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
from fb.serializers import Loginserializer, registrationserializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework import serializers
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin

# class usermodelviewset(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = userserializer
#     def create(self, request, *args, **kwargs):
#         return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#     permission_classes = [IsOwnerOrReadOnly]


class Usermodelviewset(GenericAPIView,ListModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = userserializer

    def get(self,request,*args,**kwargs):
        return self.list(request,*args,**kwargs)




class UsermodelviewsetRUD(GenericAPIView,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = userserializer

    def get(self,request,*args,**kwargs):
        return self.retrieve(request,*args,**kwargs)


    def put(self,request,*args,**kwargs):
        return self.update(request,*args,**kwargs)


    def delete(self,request,*args,**kwargs):
        return self.destroy(request,*args,**kwargs)

    permission_classes = [IsOwnerOrReadOnly]


    


class Postmodelviewset(viewsets.ModelViewSet):
    queryset = CreatePost.objects.all()
    serializer_class = postserializer
    permission_classes = [IsOwnerOrReadOnly]
    def update (self, request, *args, **kwargs):
        instance=self.get_object()
        data=request.data.copy()
        if 'image' not in data or data.get('image') in [None, '','null']:
            data['image']=instance.image
        serializer=self.get_serializer(instance,data=data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user.userprofile)

    def get_like_count(self,obj):
    	return getattr(obj,'like_count',obj.likes.count())

    @action(detail=True, methods=['post'], url_path='likes', permission_classes=[IsAuthenticated])
    def like_unlike(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'message': 'Post liked'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='likes', permission_classes=[IsAuthenticated])
    def liked_posts(self, request):
        user = request.user
        posts = CreatePost.objects.filter(likes=user)
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class Commentmodelviewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = commentserializer
    permission_classes = [IsOwnerOrReadOnly]
    def perform_create(self,serializer):
    	serializer.save(user=self.request.user)


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
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid or expired refresh token'}, status=status.HTTP_400_BAD_REQUEST)




