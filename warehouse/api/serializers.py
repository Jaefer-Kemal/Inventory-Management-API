from rest_framework import serializers
from inventory.models import Warehouse
# Serializer for Warehouse
class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'address', 'country', 'city', 'state', 'postal_code', 'image', 'created_at', 'updated_at']
