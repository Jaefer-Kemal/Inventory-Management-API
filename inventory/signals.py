from django.db.models.signals import post_save
from django.dispatch import receiver
from orders.models import PurchaseOrder, PurchaseOrderItem
from inventory.models import WarehouseStock
from warehouse.models import Warehouse  # Assuming the Warehouse model is in the warehouse app

@receiver(post_save, sender=PurchaseOrder)
def update_warehouse_stock(sender, instance, **kwargs):
    # Check if the status has changed to 'confirmed'
    if instance.status == 'confirmed':
        # Get the default warehouse (or customize based on your logic)
        warehouse = Warehouse.objects.get(pk=1)  # Change this if needed

        # Loop through the related PurchaseOrderItems
        for item in instance.items.all():
            product = item.product
            quantity = item.quantity

            # Get or create the stock record for the product in the warehouse
            stock, created = WarehouseStock.objects.get_or_create(
                product=product,
                warehouse=warehouse
            )

            # Update the stock quantity
            stock.quantity += quantity
            stock.save()

        print(f"Stock updated for Purchase Order {instance.id} in warehouse {warehouse.id}")
