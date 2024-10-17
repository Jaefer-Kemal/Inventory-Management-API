from django.contrib import admin
from .models import Warehouse

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'state', 'country', 'postal_code', 'created_at', 'updated_at')  # Fields displayed in the list view
    search_fields = ('name', 'city', 'country')  # Searchable fields
    list_filter = ('country', 'city', 'state')  # Filter options in the sidebar
    ordering = ('name',)  # Default ordering in the admin list view
    readonly_fields = ('created_at', 'updated_at')  # Non-editable fields
    fields = ('name', 'address', 'city', 'state', 'postal_code', 'country', 'image', 'created_at', 'updated_at')  # Fields layout

    def full_address(self, obj):
        return obj.full_address
    full_address.short_description = 'Full Address'  # Rename column header in the admin site
