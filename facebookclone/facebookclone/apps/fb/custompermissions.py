# from rest_framework.permissions import BasePermission

# class Mypermission(BasePermission):
# 	def has_permission(self,request,views):
# 		if request.method=="GET":
# 			return True 

# 	def update(self, instance, validated_data):
# 		request = self.context.get("request")
# 		if instance.author.id==request.user.id:
# 			instance.save()

	

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
        	return True
        return obj.user == request.phone_number