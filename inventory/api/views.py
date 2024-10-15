from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductTransferSerializer
from inventory.functions import transfer_product
from django.core.exceptions import ObjectDoesNotExist
from inventory.models import Product, WarehouseStock, Category
from inventory.api.serializers import ProductSerializer, WarehouseStockSerializer, CategorySerializer

# Product Views
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# Warehouse Stock Views
class WarehouseStockListView(generics.ListCreateAPIView):
    queryset = WarehouseStock.objects.all()
    serializer_class = WarehouseStockSerializer

class WarehouseStockDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WarehouseStock.objects.all()
    serializer_class = WarehouseStockSerializer

class Category()

class ProductTransferView(APIView):
    def post(self, request):
        serializer = ProductTransferSerializer(data=request.data)

        if serializer.is_valid():
            source_warehouse_id = serializer.validated_data['source_warehouse_id']
            destination_warehouse_id = serializer.validated_data['destination_warehouse_id']
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            try:
                # Call the transfer_product function
                transfer_product(source_warehouse_id, destination_warehouse_id, product_id, quantity)
                return Response({"message": "Product transferred successfully."}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist as e:
                return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
