# serializers.py

from django.db import transaction
from rest_framework import serializers
from inventory.models import Product
from orders.models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem
from inventory.models import WarehouseStock
from warehouse.models import Warehouse

class PurchaseOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Ensure the product exists

    class Meta:
        model = PurchaseOrderItem
        fields = ["product", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = PurchaseOrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    created_by = serializers.ReadOnlyField(source='created_by.username')
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = PurchaseOrder
        fields = [
            "id",
            "created_by",
            "status",
            "is_active",
            "created_at",
            "updated_at",
            "items",
            "total_amount",
        ]

    def create(self, validated_data):
        # Pop the items data before creating the PurchaseOrder
        items_data = validated_data.pop("items", None)

        # Set initial status and is_active flags
        validated_data["status"] = "pending"
        validated_data["is_active"] = True

        # Create the PurchaseOrder instance
        purchase_order = PurchaseOrder.objects.create(**validated_data)

        # Create related PurchaseOrderItem instances
        if items_data:
            for item_data in items_data:
                PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order, **item_data
                )

        return purchase_order

    def update(self, instance, validated_data):
        # Check the status change
        new_status = validated_data.get("status", instance.status)
        


        # Prevent specific status changes as per business rules
        if instance.status == "pending" and new_status in ["completed", "cancelled"]:
            raise serializers.ValidationError(
                "Order must be approved before it can be completed or cancelled."
            )
        if instance.status == "approved" and new_status == "pending":
            raise serializers.ValidationError(
                "Cannot revert an approved order to pending."
            )


        # Handle items update logic
        items_data = validated_data.pop("items", None)
        if instance.status == "pending" and items_data:
            # If still pending, we can modify the items
            instance.items.all().delete()  # Remove old items
            for item_data in items_data:
                PurchaseOrderItem.objects.create(
                    purchase_order=instance, **item_data
                )
        elif instance.status in ["approved", "completed", "cancelled"]:
            if items_data:
                raise serializers.ValidationError(
                    "You cannot modify items after the order is approved or completed."
                )
                
        if (items_data==[]) and (new_status=="approved"):
            raise serializers.ValidationError("You cannot approve empty items")

        # Handle soft-delete logic
        if new_status in ["cancelled", "completed"]:
            instance.is_active = False
        
        if new_status == "completed":
            # Always refer to warehouse with ID=1
            warehouse = Warehouse.objects.get(id=1)

            # Loop through the items and update stock in the warehouse
            for item in instance.items.all():
                product = item.product
                quantity = item.quantity
                
                # Find or create the corresponding WarehouseStock record for warehouse with ID=1
                warehouse_stock, created = WarehouseStock.objects.get_or_create(
                    product=product,
                    warehouse=warehouse,
                    defaults={"quantity": 0}  # In case it's newly created, start with 0
                )
                
                # Increase the quantity in the warehouse
                warehouse_stock.quantity += quantity
                warehouse_stock.save()    
        # Update the status and save the order
        instance.status = new_status
        instance.save()

        return instance


class SalesOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )  # Ensure the product exists

    class Meta:
        model = SalesOrderItem
        fields = ["product", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value



class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customer = serializers.ReadOnlyField(source='customer.user.username')
    is_active = serializers.ReadOnlyField()
    class Meta:
        model = SalesOrder
        fields = ['id', 'customer', 'status', 'is_active', 'created_at', 'updated_at', 'items', 'total_amount']

    def create(self, validated_data):
        # Extract items data before creating the SalesOrder
        items_data = validated_data.pop('items', [])
        
        # Automatically set the status and is_active flags
        validated_data['status'] = 'pending'
        validated_data['is_active'] = True

        # Create the SalesOrder instance
        sales_order = SalesOrder.objects.create(**validated_data)

        # Create related SalesOrderItem instances
        for item_data in items_data:
            SalesOrderItem.objects.create(sales_order=sales_order, **item_data)

        return sales_order


    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        # Prevent changing status from approved to pending
        if instance.status == 'approved' and new_status == 'pending':
            raise serializers.ValidationError("Cannot revert an approved order to pending.")

        items_data = validated_data.pop('items', None)

        if instance.status == 'pending':
            if items_data is not None:  # Check if items_data is provided
                instance.items.all().delete()  # Remove old items
                self._create_sales_order_items(instance, items_data)
        elif instance.status in ['completed', 'cancelled', 'approved']:
            if items_data is not None:  # Check if items_data is provided
                raise serializers.ValidationError(
                    f"You can't modify items once it's {instance.status}"
                )

        # Handle stock deduction and return logic
        if new_status == 'approved':
            self._validate_stock_availability(items_data or [])
            self._deduct_stock(instance)

        if new_status == 'cancelled':
            self._return_stock(instance)

        if new_status in ['cancelled', 'completed']:
            instance.is_active = False

        if (items_data==[]) and (new_status=="approved"):
            raise serializers.ValidationError("You cannot approve empty items")
        # Update the status and save the order
        instance.status = new_status
        instance.save()

        return instance

    def _create_sales_order_items(self, sales_order, items_data):
        for item_data in items_data:
            SalesOrderItem.objects.create(sales_order=sales_order, **item_data)

    def _validate_stock_availability(self, items_data):
        for item_data in items_data:
            quantity_needed = item_data['quantity']
            product = item_data['product']
            
            # Check total quantity available across all warehouse stocks
            total_available = sum(
                warehouse_stock.quantity for warehouse_stock in WarehouseStock.objects.filter(product=product)
            )
            if total_available < quantity_needed:
                raise serializers.ValidationError(f"Insufficient stock for product {product}. Available: {total_available}, Required: {quantity_needed}")

    def _deduct_stock(self, order):
    # Using atomic transaction to ensure data integrity
        with transaction.atomic():
            for item in order.items.all():
                product_stock_entries = WarehouseStock.objects.filter(product=item.product)
                quantity_needed = item.quantity

                for stock in product_stock_entries:
                    if quantity_needed <= 0:
                        break  # Exit if no more quantity is needed

                    if stock.quantity > 0:
                        if stock.quantity >= quantity_needed:
                            stock.quantity -= quantity_needed  # Fulfill the order
                            stock.save()
                            quantity_needed = 0  # Order fully fulfilled
                        else:
                            quantity_needed -= stock.quantity  # Use available stock
                            stock.quantity = 0  # All available stock used
                            stock.save()

                # If still need quantity after checking all stocks
                if quantity_needed > 0:
                    # Rollback previous deductions if stock is insufficient
                    for stock in product_stock_entries:
                        stock.quantity += (item.quantity - quantity_needed)  # Restore the excess
                        stock.save()

                    # Raise an error indicating insufficient stock
                    raise serializers.ValidationError(
                        f"Not enough stock to approve the order for product {item.product}."
                    )

    def _return_stock(self, order):
        for item in order.items.all():
            product_stock, created = WarehouseStock.objects.get_or_create(
                product=item.product,
                warehouse=1  # Assuming warehouse ID is 1
            )
            product_stock.quantity += item.quantity
            product_stock.save()