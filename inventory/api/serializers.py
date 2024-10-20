from rest_framework import serializers
from inventory.models import Category, Product, ProductImage, Warehouse, WarehouseStock
from users.models import Supplier

# Serializer for Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class ProductImageUploadSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(),  # Still use ImageField to accept uploads
        write_only=True
    )

    def validate_images(self, value):
        if len(value) > 3:
            raise serializers.ValidationError("You can only upload a maximum of 3 images.")
        return value

    def create(self, validated_data):
        images = validated_data.get('images')
        product = validated_data.get('product')  # Fetch product from validated data

        # Check if the product already has 3 images
        existing_images_count = ProductImage.objects.filter(product=product).count()
        if existing_images_count + len(images) > 3:
            raise serializers.ValidationError(f"Adding {len(images)} images exceeds the 3-image limit for this product.")

        # Create multiple ProductImage instances for each image
        image_instances = []
        for image in images:
            # Create a new ProductImage instance with Cloudinary image
            image_instance = ProductImage(product=product, image=image)
            image_instances.append(image_instance)

        # Bulk create images
        ProductImage.objects.bulk_create(image_instances)

        # Return all images for this product
        return ProductImage.objects.filter(product=product)

class ProductImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image']

    def validate(self, data):
        product = data['product']
        if product.images.count() >= 3:
            raise serializers.ValidationError("A product can have a maximum of 3 images.")
        return data
    


# Serializer for Warehouse Stock
class WarehouseStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WarehouseStock
        fields = ['id', 'product', 'warehouse', 'quantity']
        
    def to_representation(self, instance):
        # Get the original representation
        representation = super().to_representation(instance)

        # Modify product and warehouse fields to show their names
        representation['product'] = {"p_id":instance.product.id,
            "p_name":instance.product.name,}  # Assuming Product has a 'name' field
        representation['warehouse'] = {"w_id":instance.warehouse.id,
            "w_name":instance.warehouse.name,}  # Assuming Warehouse has a 'name' field

        return representation


# Serializer for Product with automatic warehouse assignment to Warehouse 1
class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, required=False)
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all(), required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), required=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'supplier', 'category', 'unit_price', 'reorder_level', 'images']

    # Override create method to handle warehouse stock and images
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])  # Pop the images data if provided
        product = Product.objects.create(**validated_data)

        # Automatically assign product to Warehouse 1
        warehouse, created = Warehouse.objects.get_or_create(id=1)  # Warehouse 1 must exist in the DB
        WarehouseStock.objects.create(product=product, warehouse=warehouse, quantity=0) 
        
        # Handle product images (max 3)
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)

        return product

    # Add validation for the number of images (max 3)
    def validate_images(self, images):
        if len(images) > 3:
            raise serializers.ValidationError("A product can have a maximum of 3 images.")
        return images



class ProductTransferSerializer(serializers.Serializer):
    source_warehouse_id = serializers.IntegerField()
    destination_warehouse_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value