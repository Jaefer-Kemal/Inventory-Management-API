from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from orders.models import PurchaseOrder, PurchaseOrderItem, SalesOrder, SalesOrderItem
from orders.api.serializers import (
    PurchaseOrderSerializer,
    PurchaseOrderItemSerializer,
    SalesOrderSerializer,
    SalesOrderItemSerializer,
)


# PurchaseOrder ViewSet
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated]  # Ensure authenticated access only

    def perform_create(self, serializer):
        # Set the created_by field to the currently logged-in user
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
        if purchase_order.status != "approved":
            return Response(
                {"detail": "You can only add items to an approved order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items_data = request.data.get("items", [])
        if not items_data:
            return Response(
                {"detail": "You must provide items to add."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and add the new items
        serializer = PurchaseOrderItemSerializer(data=items_data, many=True)
        serializer.is_valid(raise_exception=True)

        for item_data in items_data:
            PurchaseOrderItem.objects.create(purchase_order=purchase_order, **item_data)

        return Response(
            {"detail": "Items added successfully."}, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        # Handle the update logic and status validation via serializer
        serializer.save()


# SalesOrder ViewSet
class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically set customer as the currently logged-in user
        serializer.save(customer=self.request.user.customer)

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

        # Only allow adding items if the order is approved
        if sales_order.status != "approved":
            return Response(
                {"detail": "You can only add items to an approved sales order."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        items_data = request.data.get("items", [])
        if not items_data:
            return Response(
                {"detail": "You must provide items to add."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and add the new items
        serializer = SalesOrderItemSerializer(data=items_data, many=True)
        serializer.is_valid(raise_exception=True)

        for item_data in items_data:
            SalesOrderItem.objects.create(sales_order=sales_order, **item_data)

        return Response(
            {"detail": "Items added successfully."}, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer):
        # Handle the update logic and status validation via serializer
        serializer.save()
