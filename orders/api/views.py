from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from orders.models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem
from orders.api.serializers import (
    PurchaseOrderSerializer,
    PurchaseOrderItemSerializer,
    SalesOrderSerializer,
    SalesOrderItemSerializer,
)
from inventory.models import Product
from orders.permissions import IsCustomer, IsStoreAdminOrStaff
from django.db import transaction
# PurchaseOrder ViewSet
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, IsStoreAdminOrStaff]  # Ensure authenticated access

    def perform_create(self, serializer):
        # Set the created_by field to the current logged-in user
        serializer.save(created_by=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the existing purchase order
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    # Custom action for adding items to an existing purchase order
    @action(detail=True, methods=["post"])
    def add_items(self, request, pk=None):
        purchase_order = self.get_object()

        # Check if the order status is approved before allowing item addition
        if purchase_order.status != "pending":
            return Response(
                {"detail": "You can only add items to a pending order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items_data = request.data.get("items", None)
    
        if not isinstance(items_data, list):
            return Response(
                {"detail": "Invalid data format. 'items' should be a list of dictionaries."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if not items_data:
            return Response(
                {"detail": "You must provide items to add."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Validate and add the new items
        for item_data in items_data:
            # Get the product instance using the provided product ID
            product_id = item_data.get("product")
            try:
                product = Product.objects.get(id=product_id)  # Fetch the product instance
            except Product.DoesNotExist:
                return Response(
                    {"detail": f"Product with id {product_id} does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if PurchaseOrderItem.objects.filter(purchase_order=purchase_order, product=product).exists():
                return Response({"error":"The Product Already Exist"})
            # Create the PurchaseOrderItem instance
            PurchaseOrderItem.objects.create(
                purchase_order=purchase_order,
                product=product,  # Assign the actual Product instance
                quantity=item_data.get("quantity")
            )

        return Response(
            {"detail": "Items added successfully."},
            status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        # Save the update and handle validation via the serializer
        serializer.save()



# SalesOrder ViewSet
class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated, IsCustomer]

    def perform_create(self, serializer):
        # Automatically set customer as the currently logged-in user
        serializer.save(customer=self.request.user.customer_profile)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the existing sales order
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    # Custom action for adding items to an existing sales order
    @action(detail=True, methods=["post"])
    def add_items(self, request, pk=None):
        sales_order = self.get_object()

        # Only allow adding items if the order is pending
        if sales_order.status != "pending":
            return Response(
                {"detail": "You can only add items to a pending sales order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items_data = request.data.get("items", [])
        if not items_data:
            return Response(
                {"detail": "You must provide items to add."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and add the new items
        for item_data in items_data:
            # Ensure that a valid product ID is provided
            product_id = item_data.get('product')
            try:
                # Get the Product instance
                product = Product.objects.get(id=product_id)
                item_data['product'] = product  # Assign the product instance to item_data
            except Product.DoesNotExist:
                return Response(
                    {"detail": f"Product with id {product_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        with transaction.atomic():
            for item_data in items_data:
                SalesOrderItem.objects.create(sales_order=sales_order, **item_data)

        return Response(
            {"detail": "Items added successfully."}, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        # Handle the update logic and status validation via serializer
        serializer.save()