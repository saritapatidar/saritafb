from rest_framework import serializers
from .models import CustomUser
from .models import CreatePost
from .models import comment

class userserializer(serializers.ModelSerializer):
	class Meta:
		model =CustomUser
		fields='__all__'


class postserializer(serializers.ModelSerializer):
	class Meta:
		model=CreatePost
		fields='__all__'

class commentserializer(serializers.ModelSerializer):
	class Meta:
		model=comment
		fields='__all__'


