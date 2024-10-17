# urls.py

from django.urls import path
from inventory.api.views import (
    ProductListView,
    ProductDetailView,
    ProductImageUploadView,
    WarehouseStockListView,
    WarehouseStockDetailView,
    CategoryListView,
    CategoryDetailView,
    ProductTransferView,
)

urlpatterns = [
    # Product URLs
    path("products/", ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
    # Product image upload URL
    path("products/<int:pk>/upload-images/",ProductImageUploadView.as_view(),name="upload-product-images",),
    # Warehouse stock URLs
    path("warehouse-stocks/",WarehouseStockListView.as_view(),name="warehouse-stock-list",),
    path("warehouse-stocks/<int:pk>/",WarehouseStockDetailView.as_view(),name="warehouse-stock-detail",),
    # Category URLs
    path("categories/", CategoryListView.as_view(), name="category-list"),
    path("categories/<int:pk>/", CategoryDetailView.as_view(), name="category-detail"),
    # Product transfer URL
    path("product-transfer/", ProductTransferView.as_view(), name="product-transfer"),
]
