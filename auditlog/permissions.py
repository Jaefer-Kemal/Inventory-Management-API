# permissions.py
from rest_framework import permissions

class IsCustomerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow customers to view their own sales orders,
    while admins and staff can view all sales orders.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.role == "supplier":
            return False
        # If the user is a customer, they can only view their own orders
        if request.user.role == "customer":
            return obj.customer_name == request.user.customer_profile.name  # Adjust this according to your model field
        # If the user is an admin, store manager, or staff, they can view any order
        return request.user.role in ["admin", "store_manager", "staff"]
