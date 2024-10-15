from django.urls import path
from inventory.api.views import (
    ProductListView, ProductDeatilView,
    WarehouseStockListView, WarehouseStockDeatilView
)

urlpatterns = [
    # Product URLs
    path('products/', ProductListView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDeatilView.as_view(), name='product-detail'),

   

    # Warehouse Stock URLs
    path('warehouse-stocks/', WarehouseStockListView.as_view(), name='warehouse-stock-list-create'),
    path('warehouse-stocks/<int:pk>/', WarehouseStockDeatilView.as_view(), name='warehouse-stock-detail'),
]
