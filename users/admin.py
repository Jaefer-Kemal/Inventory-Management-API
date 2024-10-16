from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, AcessCode, Supplier, Customer, UserRank, Address


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Define the fields to be used in displaying the CustomUser model.
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "role",
        "is_active",
        "is_staff",
    )
    list_filter = ("is_staff", "is_active", "role")
    ordering = ("email",)
    search_fields = (
        "email",
        "username",
    )

    # The fields that will be displayed in the form for creating and editing a user.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("username", "first_name", "last_name", "role")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_verified")}),
    )

    # Add these fields to the "Add User" form
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
    )


@admin.register(AcessCode)
class AcessCodeAdmin(admin.ModelAdmin):
    list_display = ("role", "code")


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("user", "company_name", "phone_number")


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number")


@admin.register(UserRank)
class RankAdmin(admin.ModelAdmin):
    list_display = ("rank",)
    
@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("country",)
