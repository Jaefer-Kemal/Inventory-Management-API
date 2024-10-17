# serializers.py
from rest_framework import serializers
from auditlog.models import PurchaseOrderHistory, SalesOrderHistory, WarehouseStockHistory

class PurchaseOrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrderHistory
        fields = '__all__'  # You can also specify individual fields if needed

class SalesOrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderHistory
        fields = '__all__'

class WarehouseStockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseStockHistory
        fields = '__all__'
