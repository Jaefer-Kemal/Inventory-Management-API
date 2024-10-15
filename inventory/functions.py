from django.db import transaction
from inventory.models import WarehouseStock, Product
from warehouse.models import Warehouse
from django.core.exceptions import ObjectDoesNotExist

def transfer_product(source_warehouse_id, destination_warehouse_id, product_id, quantity):
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

        # Add stock to the destination warehouse
        destination_stock, created = WarehouseStock.objects.get_or_create(
            warehouse=destination_warehouse, 
            product=product,
            defaults={'quantity': 0}
        )
        destination_stock.quantity += quantity
        destination_stock.save()

    return {"message": "Product transferred successfully."}
