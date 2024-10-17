from django.db import transaction
from inventory.models import WarehouseStock, Product
from warehouse.models import Warehouse
from django.core.exceptions import ObjectDoesNotExist
from auditlog.models import WarehouseStockHistory
from django.utils import timezone
def transfer_product(source_warehouse_id, destination_warehouse_id, product_id, quantity):
    if source_warehouse_id == destination_warehouse_id:
        raise ValueError("Souce and Destination should not be equal")
    try:
        source_warehouse = Warehouse.objects.get(id=source_warehouse_id)
    except Warehouse.DoesNotExist:
        raise ObjectDoesNotExist(f"Source warehouse with ID {source_warehouse_id} does not exist.")
    
    try:
        destination_warehouse = Warehouse.objects.get(id=destination_warehouse_id)
    except Warehouse.DoesNotExist:
        raise ObjectDoesNotExist(f"Destination warehouse with ID {destination_warehouse_id} does not exist.")

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        raise ObjectDoesNotExist(f"Product with ID {product_id} does not exist.")

    with transaction.atomic():  # Ensure all database operations are atomic
        source_stock = WarehouseStock.objects.get(warehouse=source_warehouse, product=product)

        if source_stock.quantity < quantity:
            raise ValueError("Insufficient stock in the source warehouse.")

        # Deduct stock from the source warehouse
        source_stock.quantity -= quantity
        source_stock.save()
        WarehouseStockHistory.objects.create(
            warehouse_name=source_warehouse.name,
            products={product.id: product.name},
            quantities={product.id: quantity},
            action='transfer-out',  # Specify the transfer action
            timestamp=timezone.now(),
        )
        # Add stock to the destination warehouse
        destination_stock, created = WarehouseStock.objects.get_or_create(
            warehouse=destination_warehouse, 
            product=product,
            defaults={'quantity': 0}
        )
        destination_stock.quantity += quantity
        destination_stock.save()
        
        WarehouseStockHistory.objects.create(
                warehouse_name=destination_warehouse.name,
                products={product.id: product.name},
                quantities={product.id: quantity},
                action='transfer-in',  # Specify the transfer action
                timestamp=timezone.now(),
            )
    return {"message": "Product transferred successfully."}
