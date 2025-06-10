from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow users to edit/delete only their own objects.
    """

    def has_permission(self, request, view):
        # Allow only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        
        if hasattr(obj, 'user'):  
            return obj.user == request.user or getattr(obj.user, 'user', None) == request.user
        return obj == request.user  # For CustomUser model
# or getattr(obj.user, 'user', None) == request.user