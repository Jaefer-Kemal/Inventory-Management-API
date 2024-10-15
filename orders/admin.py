from django.contrib import admin
from orders.models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem

# Inline model to display the order items within the purchase order
class PurchaseOrderItemInline(admin.TabularInline):
    model = PurchaseOrderItem
    extra = 1  # To allow one empty form to be displayed

class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_by', 'status', 'created_at', 'updated_at', 'total_amount']
    list_filter = ['status', 'created_at', 'updated_at']  # Filter by status and time
    search_fields = ['created_by__username']  # Search by username of the creator
    inlines = [PurchaseOrderItemInline]  # Inline view of PurchaseOrderItems

    # Making total_amount read-only
    readonly_fields = ['total_amount']

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1  # To allow one empty form to be displayed

class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'status', 'created_at', 'updated_at', 'total_amount']
    list_filter = ['status', 'created_at', 'updated_at']  # Filter by status and time
    search_fields = ['customer__user__username']  # Search by customer username
    inlines = [SalesOrderItemInline]  # Inline view of SalesOrderItems

    # Making total_amount read-only
    readonly_fields = ['total_amount']

class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ['purchase_order', 'product', 'quantity']
    search_fields = ['purchase_order__id', 'product__name']  # Search by order ID or product name

class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ['sales_order', 'product', 'quantity']
    search_fields = ['sales_order__id', 'product__name']  # Search by order ID or product name


# Register the models in admin
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderItem, PurchaseOrderItemAdmin)
admin.site.register(SalesOrder, SalesOrderAdmin)
admin.site.register(SalesOrderItem, SalesOrderItemAdmin)
