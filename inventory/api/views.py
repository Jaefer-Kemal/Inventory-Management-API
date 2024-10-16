from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from inventory.functions import transfer_product
from django.core.exceptions import ObjectDoesNotExist
from inventory.models import Product, WarehouseStock, Category
from inventory.api.serializers import ( ProductSerializer,
                                       WarehouseStockSerializer,
                                       CategorySerializer,
                                       ProductImageUploadSerializer,
                                       ProductImageSerializer,
                                       ProductTransferSerializer)

from rest_framework.permissions import IsAdminUser, AllowAny
# Product Views
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]  # Only admin can create
        else:
            self.permission_classes = [AllowAny]  # Anyone can list
        return super().get_permissions()
    
class ProductDetailView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [IsAdminUser]  # Only admin can update
        else:
            self.permission_classes = [AllowAny]  # Anyone can retrieve
        return super().get_permissions()   
    
# Image Views
class ProductImageUploadView(generics.CreateAPIView):
    serializer_class = ProductImageUploadSerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser] 
        else:
            self.permission_classes = [AllowAny]  # Anyone can list
        return super().get_permissions()
       
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        return Response({"message": f"Please upload images for the product with ID: {pk}."}, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        product = get_object_or_404(Product, pk=pk)  
        
        # Pass the product in validated data to serializer
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            # Save images with the product instance
            created_images = serializer.create({**serializer.validated_data, 'product': product})

            # Use ProductImageSerializer to serialize the created image instances
            image_serializer = ProductImageSerializer(created_images, many=True)

            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# Warehouse Stock Views
class WarehouseStockListView(generics.ListCreateAPIView):
    queryset = WarehouseStock.objects.all()
    serializer_class = WarehouseStockSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]  # Only admin can create
        else:
            self.permission_classes = [AllowAny]  # Anyone can list
        return super().get_permissions()
    
class WarehouseStockDetailView(generics.RetrieveUpdateAPIView):
    queryset = WarehouseStock.objects.all()
    serializer_class = WarehouseStockSerializer
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [IsAdminUser]  # Only admin can update
        else:
            self.permission_classes = [AllowAny]  # Anyone can retrieve
        return super().get_permissions()   

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == "POST":
            self.permission_classes = [IsAdminUser]  # Only admin can create
        else:
            self.permission_classes = [AllowAny]  # Anyone can list
        return super().get_permissions()
    
class CategoryDetailView(generics.RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [IsAdminUser]  # Only admin can update
        else:
            self.permission_classes = [AllowAny]  # Anyone can retrieve
        return super().get_permissions()
    

class ProductTransferView(generics.CreateAPIView):
    serializer_class = ProductTransferSerializer
    def get(self, request, *args, **kwargs):
        message = {
            "message": "This endpoint allows you to transfer products between warehouses.",
            "instructions": {
                "source_warehouse_id": "The ID of the warehouse where the product is currently stored.",
                "destination_warehouse_id": "The ID of the warehouse where you want to transfer the product.",
                "product_id": "The ID of the product you wish to transfer.",
                "quantity": "The number of units of the product you wish to transfer."
            },
            "note": "Make sure that the source warehouse has sufficient stock of the product before initiating the transfer."
        }
        return Response(message, status=status.HTTP_200_OK)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
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