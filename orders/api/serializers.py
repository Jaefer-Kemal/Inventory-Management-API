# serializers.py

from django.db import transaction
from rest_framework import serializers
from inventory.models import Product
from orders.models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem
from inventory.models import WarehouseStock

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
    items = PurchaseOrderItemSerializer(many=True, write_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    created_by = serializers.ReadOnlyField(source='created_by.username')
    
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
        # New orders should always start as 'pending' with 'is_active' set to True
        validated_data["status"] = "pending"
        validated_data["is_active"] = True

        # Create the PurchaseOrder instance
        purchase_order = super().create(validated_data)

        # Create related PurchaseOrderItem instances
        items_data = validated_data.pop("items", None)
        if items_data:
            for item_data in items_data:
                PurchaseOrderItem.objects.create(
                    purchase_order=purchase_order, **item_data
                )

        return purchase_order

    def update(self, instance, validated_data):
        new_status = validated_data.get("status", instance.status)

        # Check if items exist when attempting to approve the order
        if new_status == "approved" and instance.items.count() == 0:
            raise serializers.ValidationError("Cannot approve an order with no items.")

        # Prevent status jump: can't go from 'pending' to 'confirmed' or 'cancelled'
        if instance.status == "pending" and new_status in ["confirmed", "cancelled"]:
            raise serializers.ValidationError(
                "Order must be approved before it can be confirmed or cancelled."
            )

        # Prevent reverting an 'approved' order back to 'pending'
        if instance.status == "approved" and new_status == "pending":
            raise serializers.ValidationError(
                "Cannot revert an approved order to pending."
            )

        # Handle soft-delete if the status changes to 'cancelled'
        if new_status == "cancelled" or new_status == "confirmed":
            instance.is_active = False

        # Handle items logic based on status
        items_data = validated_data.pop("items", None)

        if instance.status == "pending":
            # If not yet approved, you can modify items fully
            if items_data:
                instance.items.all().delete()  # Remove old items
                for item_data in items_data:
                    PurchaseOrderItem.objects.create(
                        purchase_order=instance, **item_data
                    )

        elif instance.status in ["confirmed", "cancelled", "approved"]:
            if item_data:
                raise serializers.ValidationError(
                    f"You can't modify items once it's {instance.status}"
                )

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
    items = SalesOrderItemSerializer(many=True, write_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    customer = serializers.ReadOnlyField(source='customer.username')
    
    class Meta:
        model = SalesOrder
        fields = ['id', 'customer', 'status', 'is_active', 'created_at', 'updated_at', 'items', 'total_amount']

    def create(self, validated_data):
        validated_data['status'] = 'pending'
        validated_data['is_active'] = True
        sales_order = super().create(validated_data)
        self._create_sales_order_items(sales_order, validated_data.pop('items', []))
        return sales_order

    def update(self, instance, validated_data):
        new_status = validated_data.get('status', instance.status)

        # Deactivate order on cancellation or confirmation
        if new_status in ['cancelled', 'confirmed']:
            instance.is_active = False

        # Prevent changing status from approved to pending
        if instance.status == 'approved' and new_status == 'pending':
            raise serializers.ValidationError("Cannot revert an approved order to pending.")

        items_data = validated_data.pop('items', None)

        if instance.status == 'pending':
            # If not yet approved, you can modify items fully
            if items_data:
                instance.items.all().delete()  # Remove old items
                self._create_sales_order_items(instance, items_data)
        elif instance.status in ['confirmed', 'cancelled', 'approved']:
            if items_data:
                raise serializers.ValidationError(
                    f"You can't modify items once it's {instance.status}"
                )

        # Handle stock deduction on approval
        if new_status == 'approved':
            self._validate_stock_availability(items_data)
            self._deduct_stock(instance)

        # Handle stock return on cancellation
        if new_status == 'cancelled':
            self._return_stock(instance)

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
        with transaction.atomic():
            for item in order.items.all():
                product_stock_entries = WarehouseStock.objects.filter(product=item.product)
                quantity_needed = item.quantity

                for stock in product_stock_entries:
                    if quantity_needed <= 0:
                        break

                    if stock.quantity >= quantity_needed:
                        stock.quantity -= quantity_needed
                        stock.save()
                        quantity_needed = 0  # All quantity fulfilled
                    else:
                        quantity_needed -= stock.quantity
                        stock.quantity = 0  # All quantity in this stock used
                        stock.save()

                if quantity_needed > 0:
                    # Rollback previous deductions if stock is insufficient
                    for stock in product_stock_entries:
                        stock.quantity += (item.quantity - quantity_needed)  # Revert the excess
                        stock.save()
                    raise serializers.ValidationError("Not enough stock to approve the order.")

    def _return_stock(self, order):
        for item in order.items.all():
            product_stock, created = WarehouseStock.objects.get_or_create(
                product=item.product,
                warehouse=1  # Assuming warehouse ID is 1
            )
            product_stock.quantity += item.quantity
            product_stock.save()