from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser  

@admin.register(CustomUser)  
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "role",
        "is_verified",
        "date_joined"
    )
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("role",)}),)

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("role",)}),  # Include the role field in the add form
    )


