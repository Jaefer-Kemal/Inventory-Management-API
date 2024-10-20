from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from django.http import HttpRequest

class APIRootView(APIView):
    """
    API Overview to provide a list of available endpoints
    with descriptions for each.
    """

    def get(self, request: HttpRequest):
        # Define your API overview structure
        api_overview = {
            "Welcome to IMS API": "A comprehensive API for managing inventory, orders, users, and more.",
            "To Access the Admin Panel": request.build_absolute_uri(reverse("admin:index")),
            "API Documentation": {
                "Swagger UI": request.build_absolute_uri(reverse("schema-swagger-ui")),
                "ReDoc UI": request.build_absolute_uri(reverse("schema-redoc")),
            },
            "Audit Log": {
                "Purchase History": {
                    "url": request.build_absolute_uri(reverse("purchase-order-history-list")),
                    "description": "Get a list of all purchase order histories.",
                    "methods": ["GET", "POST"],
                },
                "Sales History": {
                    "url": request.build_absolute_uri(reverse("sales-order-history-list")),
                    "description": "Get a list of all sales order histories.",
                    "methods": ["GET", "POST"],
                },
                "Stock History": {
                    "url": request.build_absolute_uri(reverse("warehouse-stock-history-list")),
                    "description": "Get a list of all stock movements.",
                    "methods": ["GET", "POST"],
                },
            },
            "Inventory Management": {
                "Categories": {
                    "url": request.build_absolute_uri(reverse("category-list")),
                    "description": "Manage product categories.",
                    "methods": ["GET", "POST"],
                },
                "Products": {
                    "url": request.build_absolute_uri(reverse("product-list")),
                    "description": "Manage products in the inventory.",
                    "methods": ["GET", "POST"],
                },
                "Product Transfer": {
                    "url": request.build_absolute_uri(reverse("product-transfer")),
                    "description": "Transfer products between warehouses.",
                    "methods": ["GET", "POST"],
                },
            },
            "Orders": {
                "Purchase Orders": {
                    "url": request.build_absolute_uri(reverse("purchase-order-list")),
                    "description": "Manage purchase orders.",
                    "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                },
                "Sales Orders": {
                    "url": request.build_absolute_uri(reverse("sales-order-list")),
                    "description": "Manage sales orders.",
                    "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                },
            },
            "Warehouse": {
                "Warehouses": {
                    "url": request.build_absolute_uri(reverse("warehouse-list")),
                    "description": "Manage warehouses.",
                    "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                },
                "Warehouse Stocks": {
                    "url": request.build_absolute_uri(reverse("warehouse-stock-list")),
                    "description": "Manage stock levels in each warehouse.",
                    "methods": ["GET", "POST", "PUT", "PATCH", "DELETE"],
                },
            },
            "Users & Roles": {
                "Access Codes": {
                    "url": request.build_absolute_uri(reverse("access_code_list_create")),
                    "description": "Generate and manage access codes for different roles.",
                    "methods": ["GET", "POST", "DELETE"],
                },
                "User Register": {
                    "Customer": {
                        "url": request.build_absolute_uri(reverse("customer-register")),
                        "description": "Register a new customer.",
                        "methods": ["GET", "POST"],
                    },
                    "Employee": {
                        "url": request.build_absolute_uri(reverse("employee-register")),
                        "description": "Register a new employee.",
                        "methods": ["GET", "POST"],
                    },
                    "Supplier": {
                        "url": request.build_absolute_uri(reverse("supplier-register")),
                        "description": "Register a new supplier.",
                        "methods": ["GET", "POST"],
                    },
                },
            },
            "Token Authentication": {
                "Token": {
                    "url": request.build_absolute_uri(reverse("token_obtain_pair")),
                    "description": "Obtain a JWT token for authentication.",
                    "methods": ["POST"],
                },
                "Refresh Token": {
                    "url": request.build_absolute_uri(reverse("token_refresh")),
                    "description": "Refresh an expired token.",
                    "methods": ["POST"],
                },
            },
        }

        # Return the API overview response
        return Response(api_overview, status=status.HTTP_200_OK)
