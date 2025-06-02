from rest_framework import serializers
from fb.models import CustomUser
from fb.models import CreatePost
from fb.models import comment

class userserializer(serializers.ModelSerializer):
	class Meta:
		model =CustomUser
		fields=['firstname','lastname','Date_of_birth','email','phone_number']


class postserializer(serializers.ModelSerializer):
	class Meta:
		model=CreatePost
		fields='__all__'
		read_only_fields=['created_at','user','likes']

class commentserializer(serializers.ModelSerializer):
	class Meta:
		model=comment
		fields='__all__'
		read_only_fields=['created_at','user']
        
class registrationserializer(serializers.ModelSerializer):
	class Meta:
		model=CustomUser
		# field=['firstname','lastname','Date_of_birth','email','phone_number','password']
		fields='__all__'
		read_only_fields=['is_active','is_staff','is_superuser']

class Loginserializer(serializers.Serializer):
	class Meta:
		model=CustomUser
		field=['phone_number','password']

	

# class Loginserializer(serializers.ModelSerializer):
# 	class Meta:
# 		model=CustomUser
# 		fields=['phone_number','password']