from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from warehouse.models import Warehouse
from warehouse.api.serializers import WarehouseSerializer
from inventory.models import WarehouseStock
from inventory.api.serializers import ProductSerializer
from rest_framework.permissions import IsAdminUser
# Warehouse Views
class WarehouseListView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdminUser]

class WarehouseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAdminUser]

# product in that warehouse
class WarehouseProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    
    def get(self, request, pk, *args, **kwargs):
        warehouse = get_object_or_404(Warehouse, pk=pk)
        # Fetch all the products in this warehouse
        warehouse_stocks = WarehouseStock.objects.filter(warehouse=warehouse)
        # Check if there are products in the warehouse
        if not warehouse_stocks.exists():
            return Response({"message": "There are no products in this warehouse."}, status=status.HTTP_200_OK)
        products = [stock.product for stock in warehouse_stocks]
        
        # Serialize the product data
        serializer = self.get_serializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
