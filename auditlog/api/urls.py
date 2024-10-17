from django.urls import path
from .views import (
    PurchaseOrderHistoryList,
    PurchaseOrderHistoryDetail,
    SalesOrderHistoryList,
    SalesOrderHistoryDetail,
    WarehouseStockHistoryList,
    WarehouseStockHistoryDetail,
)

urlpatterns = [
    path('purchase-history/', PurchaseOrderHistoryList.as_view(), name='purchase-order-history-list'),
    path('purchase-history/<int:pk>/', PurchaseOrderHistoryDetail.as_view(), name='purchase-order-history-detail'),
    path('sales-history/', SalesOrderHistoryList.as_view(), name='sales-order-history-list'),
    path('sales-history/<int:pk>/', SalesOrderHistoryDetail.as_view(), name='sales-order-history-detail'),
    path('stock-history/', WarehouseStockHistoryList.as_view(), name='warehouse-stock-history-list'),
    path('stock-history/<int:pk>/', WarehouseStockHistoryDetail.as_view(), name='warehouse-stock-history-detail'),
]