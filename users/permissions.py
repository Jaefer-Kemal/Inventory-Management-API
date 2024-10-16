from rest_framework import permissions


class AddressPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj, method):
        # Allow access only if the address belongs to the user
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
