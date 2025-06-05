from rest_framework import serializers
from fb.models import CustomUser
from fb.models import CreatePost
from fb.models import comment
from fb.models import Like
from django.contrib.auth.hashers import make_password


class userserializer(serializers.ModelSerializer):
	class Meta:
		model =CustomUser
		fields=['id','firstname','lastname','Date_of_birth','email','phone_number','password']


class postserializer(serializers.ModelSerializer):
	like_count=serializers.SerializerMethodField()
	# user=userserializer(source='user.user.firstname')
	user=serializers.SerializerMethodField()
	class Meta:
		model=CreatePost
		fields=['id','content','image','like_count','user',]
		read_only_fields=['user']

	def get_like_count(self,obj):
		return obj.likes.count() 

	def get_user(self,obj):
		return obj.user.user.firstname


class commentserializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	class Meta:
		model=comment

		fields=['post','text','user']
		read_only_fields=['user']

	def get_user(self,obj):
		return obj.user.firstname

        
class Loginserializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)



class registrationserializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields=['firstname','lastname','Date_of_birth','gender','email','phone_number','password']

    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)



class likeserializer(serializers.ModelSerializer):
	like_count=serializers.SerializerMethodField()
	class Meta:
		model=Like
		fields=['post','liked_by','like_count']

	def get_like_count(self,obj):
		return obj.liked_by.count()
		