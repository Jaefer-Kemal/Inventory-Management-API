from rest_framework import serializers
from inventory.models import Category, Product, ProductImage, Warehouse, WarehouseStock
from users.models import Supplier

# Serializer for Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductImageUploadSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())  # Product to attach the images to
    images = serializers.ListField(  # List of image files
        child=serializers.ImageField(),
        write_only=True
    )

    def validate_images(self, value):
        if len(value) > 3:  # Ensure there are no more than 3 images
            raise serializers.ValidationError("You can upload a maximum of 3 images.")
        return value

    def create(self, validated_data):
        product = validated_data.get('product_id')  # Get the product object
        images = validated_data.get('images')  # Get the list of images

        # Check if the product already has 3 images
        existing_images_count = ProductImage.objects.filter(product=product).count()
        if existing_images_count + len(images) > 3:
            raise serializers.ValidationError(f"Adding {len(images)} images exceeds the 3-image limit for this product.")

        # Create multiple ProductImage instances for each image
        image_instances = [ProductImage(product=product, image=image) for image in images]
        
        # Bulk create images
        ProductImage.objects.bulk_create(image_instances)

        # Fetch the newly created image instances with IDs
        return ProductImage.objects.filter(product=product)  # Return all images for this product
    
    
# Serializer for Product Image with validation for maximum 3 images
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





