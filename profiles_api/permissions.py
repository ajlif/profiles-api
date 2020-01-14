from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow users to edit their own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit their own profile"""
        # safe methods dont make update to the object
        if request.method in permissions.SAFE_METHODS:
            return True

        # obj is the object that the user intend update
        return obj.id == request.user.id