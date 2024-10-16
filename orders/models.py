from django.db import models
from inventory.models import Product
from users.models import CustomUser, Customer

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
]

class PurchaseOrder(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="purchase_orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Purchase Order #{self.id} by {self.created_by.username}"

    @property
    def total_amount(self):
        total = sum(item.quantity * item.product.unit_price for item in self.items.all())  # Fixed relationship
        return total

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.product.name} (Qty: {self.quantity})"


class SalesOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="sales_orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Sales Order #{self.id} for {self.customer.user.username}"

    @property
    def total_amount(self):
        total = sum(item.quantity * item.product.unit_price for item in self.items.all())  # Similar to PurchaseOrder
        return total

class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} (Qty: {self.quantity})"
