from django.db import models
from warehouse.models import Warehouse
from users.models import Supplier
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Category Name")
    description = models.TextField(max_length=255, verbose_name="Description")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(blank=True, verbose_name="Product Description")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Supplier")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products', verbose_name="Category")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Unit Price")
    reorder_level = models.PositiveIntegerField(default=1, verbose_name="Reorder Level")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Product")
    image = CloudinaryField('image', folder='product/', blank=True, null=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"Image for {self.product.name}"
    
    # Override the delete method to ensure Cloudinary deletion
    def delete(self, *args, **kwargs):
        # If the image exists, delete it from Cloudinary
        if self.image:
            # Get the public ID of the image stored in Cloudinary
            public_id = self.image.public_id
            if public_id:
                destroy(public_id)  # Call Cloudinary API to delete the image
                print(f"Deleted {public_id} from Cloudinary.")

        # Now delete the record from the database
        super().delete(*args, **kwargs)

class WarehouseStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks', verbose_name="Product")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stocks", verbose_name="Warehouse",default=1)
    quantity = models.PositiveIntegerField(verbose_name="Quantity", default=0)

    class Meta:
        verbose_name = "Warehouse Stock"
        verbose_name_plural = "Warehouse Stocks"
        unique_together = ('product', 'warehouse')  # Ensures that a product can only have one stock entry per warehouse

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units in {self.warehouse.name}"
