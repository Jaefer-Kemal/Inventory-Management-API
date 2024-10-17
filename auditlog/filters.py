# filters.py
from django_filters import rest_framework as filters
from auditlog.models import PurchaseOrderHistory, SalesOrderHistory, WarehouseStockHistory
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

ACTION_CHOICES = [
    ('created', 'Created'),
    ('status_changed', 'Status Changed'),
    ('order_completed', 'Order Completed'),
    ('order_cancelled', 'Order Cancelled'),
]

class PurchaseOrderHistoryFilter(filters.FilterSet):
    created_by = filters.CharFilter(field_name='created_by', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=STATUS_CHOICES)
    action = filters.ChoiceFilter(choices=ACTION_CHOICES)
    year = filters.NumberFilter(field_name='timestamp__year', lookup_expr='exact')
    month = filters.NumberFilter(field_name='timestamp__month')
    day = filters.NumberFilter(field_name='timestamp__day')

    class Meta:
        model = PurchaseOrderHistory
        fields = ['created_by', 'status', 'action', 'year', 'month', 'day']

class SalesOrderHistoryFilter(filters.FilterSet):
    customer_name = filters.CharFilter(field_name='customer_name', lookup_expr='icontains')
    status = filters.ChoiceFilter(choices=STATUS_CHOICES)
    action = filters.ChoiceFilter(choices=ACTION_CHOICES)
    year = filters.NumberFilter(field_name='timestamp__year')
    month = filters.NumberFilter(field_name='timestamp__month')
    day = filters.NumberFilter(field_name='timestamp__day')

    class Meta:
        model = SalesOrderHistory
        fields = ['customer_name', 'status', 'action' , 'year', 'month', 'day']

class WarehouseStockHistoryFilter(filters.FilterSet):
    warehouse_name = filters.CharFilter(field_name='warehouse_name', lookup_expr='icontains')
    action = filters.CharFilter(field_name='action', lookup_expr='icontains')
    year = filters.NumberFilter(field_name='timestamp__year')
    month = filters.NumberFilter(field_name='timestamp__month')
    day = filters.NumberFilter(field_name='timestamp__day')

    class Meta:
        model = WarehouseStockHistory
        fields = ['warehouse_name', 'action' , 'year', 'month', 'day']
