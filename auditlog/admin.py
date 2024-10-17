from django.contrib import admin
from auditlog.models import PurchaseOrderHistory, SalesOrderHistory, WarehouseStockHistory

@admin.register(PurchaseOrderHistory)
class PurchaseOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'action', 'status', 'total_amount', 'timestamp')
    list_filter = ('status', 'action', 'timestamp')
    search_fields = ('created_by', 'products')
    ordering = ('-timestamp',)

@admin.register(SalesOrderHistory)
class SalesOrderHistoryAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'action', 'status', 'total_amount', 'timestamp')
    list_filter = ('status', 'action', 'timestamp')
    search_fields = ('customer_name', 'products')
    ordering = ('-timestamp',)

@admin.register(WarehouseStockHistory)
class WarehouseStockHistoryAdmin(admin.ModelAdmin):
    list_display = ('warehouse_name', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('warehouse_name', 'products')
    ordering = ('-timestamp',)
