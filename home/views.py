from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse

class APIRootView(APIView):
    """
    API Overview for the Inventory Management System (IMS).
    Provides a structured overview of all available endpoints, descriptions, and usage examples.
    """

    def get(self, request, *args, **kwargs):
        api_overview = {
            "Welcome to IMS API": "A comprehensive API for managing inventory, orders, users, and more.",
            "To Access the Admin Panel": request.build_absolute_uri(reverse("admin:index")),
            "Audit Log": {
                "Purchase History": {
                    "url": request.build_absolute_uri(reverse("purchase-order-history-list")),
                    "description": "Get a list of all purchase order histories.",
                    "methods": ["GET"],
                },
                "Purchase History Detail": {
                    "url": request.build_absolute_uri(reverse("purchase-order-history-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific purchase order history using its ID.",
                    "methods": ["GET"],
                },
                "Sales History": {
                    "url": request.build_absolute_uri(reverse("sales-order-history-list")),
                    "description": "Get a list of all sales order histories.",
                    "methods": ["GET"],
                },
                "Sales History Detail": {
                    "url": request.build_absolute_uri(reverse("sales-order-history-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific sales order history using its ID.",
                    "methods": ["GET"],
                },
                "Stock History": {
                    "url": request.build_absolute_uri(reverse("warehouse-stock-history-list")),
                    "description": "Get a list of all warehouse stock histories.",
                    "methods": ["GET"],
                },
                "Stock History Detail": {
                    "url": request.build_absolute_uri(reverse("warehouse-stock-history-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific stock history using its ID.",
                    "methods": ["GET"],
                },
            },
            "Inventory": {
                "List Products": {
                    "url": request.build_absolute_uri(reverse("product-list")),
                    "description": "Get a list of all available products.",
                    "methods": ["GET"],
                },
                "Product Details": {
                    "url": request.build_absolute_uri(reverse("product-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific product using its ID.",
                    "methods": ["GET"],
                },
                "Upload Product Images": {
                    "url": request.build_absolute_uri(reverse("upload-product-images", kwargs={"pk": 1})),
                    "description": "Upload images for a specific product using its ID.",
                    "methods": ["POST"],
                },
                "List Warehouse Stocks": {
                    "url": request.build_absolute_uri(reverse("warehouse-stock-list")),
                    "description": "Get a list of all warehouse stocks.",
                    "methods": ["GET"],
                },
                "Warehouse Stock Details": {
                    "url": request.build_absolute_uri(reverse("warehouse-stock-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific warehouse stock using its ID.",
                    "methods": ["GET"],
                },
                "List Categories": {
                    "url": request.build_absolute_uri(reverse("category-list")),
                    "description": "Get a list of all product categories.",
                    "methods": ["GET"],
                },
                "Category Details": {
                    "url": request.build_absolute_uri(reverse("category-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific category using its ID.",
                    "methods": ["GET"],
                },
                "Product Transfer": {
                    "url": request.build_absolute_uri(reverse("product-transfer")),
                    "description": "Transfer a product from one warehouse to another.",
                    "methods": ["POST"],
                },
            },
            "Orders": {
                "List Purchase Orders": {
                    "url": request.build_absolute_uri(reverse("purchase-order-list")),
                    "description": "Get a list of all purchase orders.",
                    "methods": ["GET"],
                },
                "Purchase Order Details": {
                    "url": request.build_absolute_uri(reverse("purchase-order-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific purchase order using its ID.",
                    "methods": ["GET"],
                },
                "List Sales Orders": {
                    "url": request.build_absolute_uri(reverse("sales-order-list")),
                    "description": "Get a list of all sales orders.",
                    "methods": ["GET"],
                },
                "Sales Order Details": {
                    "url": request.build_absolute_uri(reverse("sales-order-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific sales order using its ID.",
                    "methods": ["GET"],
                },
            },
            "Users": {
                "Employee Registration": {
                    "url": request.build_absolute_uri(reverse("employee-register")),
                    "description": "Register a new employee.",
                    "methods": ["POST"],
                },
                "Supplier Registration": {
                    "url": request.build_absolute_uri(reverse("supplier-register")),
                    "description": "Register a new supplier.",
                    "methods": ["POST"],
                },
                "Customer Registration": {
                    "url": request.build_absolute_uri(reverse("customer-register")),
                    "description": "Register a new customer.",
                    "methods": ["POST"],
                },
                "List Users": {
                    "url": request.build_absolute_uri(reverse("user-details")),
                    "description": "Get a list of all users.",
                    "methods": ["GET"],
                },
                "User Address Creation": {
                    "url": request.build_absolute_uri(reverse("address-create")),
                    "description": "Create a new address for a user.",
                    "methods": ["POST"],
                },
                "Address Details": {
                    "url": request.build_absolute_uri(reverse("address-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific address using its ID.",
                    "methods": ["GET"],
                },
                "Obtain Token": {
                    "url": request.build_absolute_uri(reverse("token_obtain_pair")),
                    "description": "Obtain a new access token using credentials.",
                    "methods": ["POST"],
                },
                "Refresh Token": {
                    "url": request.build_absolute_uri(reverse("token_refresh")),
                    "description": "Refresh an access token using a refresh token.",
                    "methods": ["POST"],
                },
            },
            "Warehouse": {
                "List Warehouses": {
                    "url": request.build_absolute_uri(reverse("warehouse-list")),
                    "description": "Get a list of all warehouses.",
                    "methods": ["GET"],
                },
                "Warehouse Details": {
                    "url": request.build_absolute_uri(reverse("warehouse-detail", kwargs={"pk": 1})),
                    "description": "Retrieve details of a specific warehouse using its ID.",
                    "methods": ["GET"],
                },
                "Warehouse Products": {
                    "url": request.build_absolute_uri(reverse("warehouse-products", kwargs={"pk": 1})),
                    "description": "Get a list of all products in a specific warehouse.",
                    "methods": ["GET"],
                },
            },
        }
        return Response(api_overview, status=status.HTTP_200_OK)
