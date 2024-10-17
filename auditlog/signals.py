from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import PurchaseOrder, SalesOrder, PurchaseOrderItem, SalesOrderItem
from auditlog.models import PurchaseOrderHistory, SalesOrderHistory, WarehouseStockHistory
from inventory.models import WarehouseStock
from django.utils import timezone

@receiver(post_save, sender=PurchaseOrder)
def log_purchase_order_history(sender, instance, created, **kwargs):
    """
    Signal to log PurchaseOrder history whenever the status changes.
    """
    # Log when a new purchase order is created
    if created:
        PurchaseOrderHistory.objects.create(
            created_by=instance.created_by.username,
            products=[],  # Empty on creation
            quantities=[],  # Empty on creation
            status=instance.status,
            action='created',  # Action is creation
            total_amount=instance.total_amount
        )
    # Log if status is changed to approved, completed, or cancelled
    elif instance.status in ['approved', 'completed', 'cancelled']:
        products = [item.product.name for item in instance.items.all()]
        quantities = [item.quantity for item in instance.items.all()]
        action = 'status_changed' if instance.status == 'approved' else f"order_{instance.status}"
        
        PurchaseOrderHistory.objects.create(
            created_by=instance.created_by.username,
            products=products,
            quantities=quantities,
            status=instance.status,
            action=action,  # Action could be 'status_changed', 'order_completed', or 'order_cancelled'
            total_amount=instance.total_amount
        )


@receiver(post_save, sender=SalesOrder)
def log_sales_order_history(sender, instance, created, **kwargs):
    """
    Signal to log SalesOrder history whenever the status changes.
    """
    # Log when a new sales order is created
    if created:
        SalesOrderHistory.objects.create(
            customer_name=instance.customer.user.username,
            products=[],  # Empty on creation
            quantities=[],  # Empty on creation
            status=instance.status,
            action='created',  # Action is creation
            total_amount=instance.total_amount
        )
    # Log if status is changed to approved, completed, or cancelled
    elif instance.status in ['approved', 'completed', 'cancelled']:
        products = [item.product.name for item in instance.items.all()]
        quantities = [item.quantity for item in instance.items.all()]
        action = 'status_changed' if instance.status == 'approved' else f"order_{instance.status}"
        
        SalesOrderHistory.objects.create(
            customer_name=instance.customer.user.username,
            products=products,
            quantities=quantities,
            status=instance.status,
            action=action,  
            total_amount=instance.total_amount
        )

@receiver(post_save, sender=WarehouseStock)
def update_warehouse_stock_history(sender, instance, created, **kwargs):
    """
    Signal to create a warehouse stock history entry whenever WarehouseStock is updated.
    """
    # If this is a transfer, history will already be handled by the transfer function
    if kwargs.get('raw', False):
        return  # Avoid creating history during data loading

    action = "created" if created else "updated"

    WarehouseStockHistory.objects.create(
        warehouse_name=instance.warehouse.name,
        products={instance.product.id: instance.product.name},
        quantities={instance.product.id: instance.quantity},
        action=action,  # Use the default action here (created or updated)
        timestamp=timezone.now(),
    )
