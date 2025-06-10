from rest_framework import serializers
from fb.models import CustomUser
from fb.models import CreatePost
from fb.models import Comment
from django.contrib.auth.hashers import make_password


class userserializer(serializers.ModelSerializer):
	class Meta:
		model =CustomUser
		fields=['id','firstname','lastname','Date_of_birth','email','phone_number','password']
		read_only_fields=['password']


class postserializer(serializers.ModelSerializer):
	like_count=serializers.SerializerMethodField()
	user=serializers.SerializerMethodField()
	class Meta:
		model=CreatePost
		fields=['id','content','image','like_count','user']
		read_only_fields=['user']

	def get_like_count(self,obj):
		return obj.likes.count() 

	def get_user(self,obj):
		return obj.user.user.firstname



class parentserializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	class Meta:
		model=Comment
		fields=['id','text','user','post']

	def get_user(self,obj):
		return obj.user.firstname



class commentserializer(serializers.ModelSerializer):
	user=serializers.SerializerMethodField()
	replies=parentserializer(many=True,read_only=True)
	class Meta:
		model=Comment
		fields=['id','post','text','user','parent','replies']
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








