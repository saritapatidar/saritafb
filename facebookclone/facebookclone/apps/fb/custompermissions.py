from rest_framework.permissions import BasePermission

class Mypermission(BasePermission):
	def has_permission(self,request,views):
		if request.method=="GET":
			return True 
