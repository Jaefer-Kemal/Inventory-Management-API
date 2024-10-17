from rest_framework import permissions

class IsCustomer(permissions.BasePermission):


    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'customer' role
        return request.user.is_authenticated and (request.user.role == "customer")
    
class IsStoreAdminOrStaff(permissions.BasePermission):


    def has_permission(self, request, view):
        # Check if the user is authenticated and has one of the allowed roles
        return request.user.is_authenticated and (
            request.user.role in ["store_manager", "admin", "staff"]
        )