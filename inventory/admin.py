from django.contrib import admin
from .models import Category, Product, ProductImage, WarehouseStock

# Category Admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')  # Fields to display in the list view
    search_fields = ('name',)  # Searchable fields
    ordering = ('name',)  # Default ordering by name


# Product Admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier', 'category', 'unit_price', 'reorder_level')
    search_fields = ('name', 'supplier__user__username')  # Searching by product name and supplier username
    list_filter = ('category', 'supplier')  # Filtering options in admin
    ordering = ('name',)  # Default ordering by product name


# Product Image Admin
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__name',)  # Searchable by product name


# Warehouse Stock Admin
@admin.register(WarehouseStock)
class WarehouseStockAdmin(admin.ModelAdmin):
    list_display = ('product', 'warehouse', 'quantity')
    search_fields = ('product__name', 'warehouse__name')  # Search by product name and warehouse name
    list_filter = ('warehouse',)  # Filter by warehouse
    ordering = ('product', 'warehouse')  # Default ordering by product and warehouse
