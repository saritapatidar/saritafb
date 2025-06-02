from django.shortcuts import render
from.custompermissions import IsOwnerOrReadOnly
# from .custompermissions import postconditions
# from rest_framework.authentication import TokenAuthentication
from .serializers import userserializer
from .serializers import postserializer
from .serializers import commentserializer,Loginserializer
from rest_framework import viewsets
from .models import CustomUser
from .models import CreatePost
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




class usermodelviewset(viewsets.ModelViewSet):
	
	queryset = CustomUser.objects.all()
	serializer_class = userserializer
	permission_classes = [IsAuthenticated]
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsOwnerOrReadOnly]


class postmodelviewset(viewsets.ModelViewSet):
    queryset = CreatePost.objects.all()
    serializer_class = postserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    

class commentmodelviewset(viewsets.ModelViewSet):
	queryset = comment.objects.all()
	serializer_class = commentserializer
	authentication_classes = [TokenAuthentication]
	permission_classes = [IsAuthenticated]
	authentication_classes = [SessionAuthentication]
	permission_classes = [IsOwnerOrReadOnly]

	def perform_create(self,serializer):
		serializer.save(user=self.request.user)


from .serializers import registrationserializer
from rest_framework import generics

class UserRegistrationView(generics.CreateAPIView):
	serializer_class = registrationserializer
	permission_classes=[AllowAny]

class Login(GenericAPIView):
	
	def post(self,request):
		serializer_class = Loginserializer
		serializer=Loginserializer(request.data)
		
		if serializer.is_valid():
			username=serializer.validated_data(phone_number=phone_number)
			password=serializer.validated_data(password=password)
			user=authenticate(phone_number=phone_number,password=password)
			if user:
				token,created=Token.objects.get_or_create(user=user)
				return response({"status":True,"data":{'token':str(token)}})
			else:
				return response({"status":False,"data":{},"message":"Invalid"})
		else:
			return response({"status":False,"error":serializer.errors,"message":"validation data"})


# class LogoutViewSet(APIView):
#     permission_classes = [IsAuthenticated] 
#     def post(self, request):
#         logout(request)
#         return Response({'message': 'Logout successful'})


# from rest_framework.permissions import AllowAny, IsAuthenticated

# class LoginViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticated] 
#     def create(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user:
#             login(request, user)
#             return Response({'message': 'Login successful'})
#         else:
#             return Response({'message': 'Invalid credentials'}, status=401)



   
class LogoutAPI(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		request.user.auth_token.delete()
		return Response(status=status.HTTP_200_OK)