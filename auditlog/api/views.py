# views.py
from django_filters.rest_framework import DjangoFilterBackend
from auditlog.filters import (
    PurchaseOrderHistoryFilter,
    SalesOrderHistoryFilter,
    WarehouseStockHistoryFilter,
)
from rest_framework import generics
from rest_framework import permissions
from auditlog.models import PurchaseOrderHistory, SalesOrderHistory, WarehouseStockHistory
from auditlog.api.serializers import (
    PurchaseOrderHistorySerializer,
    SalesOrderHistorySerializer,
    WarehouseStockHistorySerializer,
)
from orders.permissions import IsStoreAdminOrStaff
from auditlog.permissions import IsCustomerOrAdmin

class PurchaseOrderHistoryList(generics.ListAPIView):
    queryset = PurchaseOrderHistory.objects.all()
    serializer_class = PurchaseOrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreAdminOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PurchaseOrderHistoryFilter

class PurchaseOrderHistoryDetail(generics.RetrieveAPIView):
    queryset = PurchaseOrderHistory.objects.all()
    serializer_class = PurchaseOrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreAdminOrStaff]

class SalesOrderHistoryList(generics.ListAPIView):
    serializer_class = SalesOrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SalesOrderHistoryFilter


class SalesOrderHistoryDetail(generics.RetrieveAPIView):
    queryset = SalesOrderHistory.objects.all()
    serializer_class = SalesOrderHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrAdmin]

class WarehouseStockHistoryList(generics.ListAPIView):
    queryset = WarehouseStockHistory.objects.all()
    serializer_class = WarehouseStockHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreAdminOrStaff]
    filter_backends = [DjangoFilterBackend]
    filterset_class = WarehouseStockHistoryFilter

class WarehouseStockHistoryDetail(generics.RetrieveAPIView):
    queryset = WarehouseStockHistory.objects.all()
    serializer_class = WarehouseStockHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsStoreAdminOrStaff]
