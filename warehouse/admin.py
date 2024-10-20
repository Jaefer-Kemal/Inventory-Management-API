from django.contrib import admin
from .models import Warehouse
from django.http import HttpResponseRedirect
from cloudinary.uploader import destroy

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'postal_code', 'created_at', 'updated_at',"full_address")  # Fields displayed in the list view
    search_fields = ('name', 'city', 'country')  # Searchable fields
    list_filter = ('country', 'city', 'state')  # Filter options in the sidebar
    ordering = ('name',)  # Default ordering in the admin list view
    readonly_fields = ('created_at', 'updated_at')  # Non-editable fields
    fields = ('name', 'address', 'city', 'state', 'postal_code', 'country', 'image', 'created_at', 'updated_at')  # Fields layout

    def full_address(self, obj):
        return obj.full_address
    full_address.short_description = 'Full Address'  # Rename column header in the admin site
    
    def delete_image_from_cloudinary(self, request, queryset):
        for obj in queryset:
            if obj.image:  # Ensure the image exists
                public_id = obj.image.public_id
                destroy(public_id)  # This will delete the image from Cloudinary
                self.message_user(request, f"Image with ID {public_id} deleted from Cloudinary.")
            else:
                self.message_user(request, f"No image available for image ID {obj.id}.", level='error')

    delete_image_from_cloudinary.short_description = 'Delete selected Warehouse images from Cloudinary'

    # Add custom delete action
    actions = [delete_image_from_cloudinary]