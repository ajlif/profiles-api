from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        # safe methods ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj is the object that the user intend update
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to edit their own status"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to update their own status"""
        # safe methods ('GET', 'HEAD', 'OPTIONS')
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj is the object that the user intend update
        return obj.user_profile.id == request.user.id

