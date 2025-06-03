from rest_framework import serializers
from fb.models import CustomUser
from fb.models import CreatePost
from fb.models import comment
from fb.models import Like

class userserializer(serializers.ModelSerializer):
	class Meta:
		model =CustomUser
		fields=['id','firstname','lastname','Date_of_birth','email','phone_number']


class postserializer(serializers.ModelSerializer):
	like_count=serializers.SerializerMethodField()
	class Meta:
		model=CreatePost
		fields='__all__'
		read_only_fields=['created_at','user','likes']

	def get_like_count(self,obj):
		return obj.likes.count()

class likeserializer(serializers.ModelSerializer):
	like_count=serializers.SerializerMethodField()
	class Meta:
		model=Like
		fields=['id','post','liked_by','like_count']

	def get_like_count(self,obj):
		return obj.liked_by.count()

class commentserializer(serializers.ModelSerializer):
	class Meta:
		model=comment
		fields='__all__'
		read_only_fields=['created_at']
        
class registrationserializer(serializers.ModelSerializer):
	class Meta:
		model=CustomUser
		# field=['firstname','lastname','Date_of_birth','email','phone_number','password']
		fields='__all__'
		read_only_fields=['is_active','is_staff','is_superuser']

class Loginserializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(write_only=True)


# class Loginserializer(serializers.ModelSerializer):
# 	class Meta:
# 		model=CustomUser
# 		fields=['phone_number','password']