from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone

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

# Historical model for Purchase Orders
class PurchaseOrderHistory(models.Model):
    created_by = models.CharField(max_length=255)
    products = models.JSONField()  # List of product names
    quantities = models.JSONField() # List of quantities per product
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)  # Action that triggered the log
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Purchase Order by {self.created_by} - {self.action} on {self.timestamp}"

# Historical model for Sales Orders
class SalesOrderHistory(models.Model):
    customer_name = models.CharField(max_length=255)
    products = models.JSONField()
    quantities = models.JSONField()
    # products = ArrayField(models.CharField(max_length=255))
    # quantities = ArrayField(models.PositiveIntegerField())
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Sales Order for {self.customer_name} - {self.action} on {self.timestamp}"

# Historical model for Warehouse Stock Updates
class WarehouseStockHistory(models.Model):
    warehouse_name = models.CharField(max_length=255)
    products = models.JSONField()
    quantities = models.JSONField()
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Stock Update for {self.warehouse_name} - {self.action} on {self.timestamp}"
