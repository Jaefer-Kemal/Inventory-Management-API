from django.db import models
from warehouse.models import Warehouse
from users.models import Supplier

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
    image = models.ImageField(upload_to="product_images/", verbose_name="Image")

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

    def __str__(self):
        return f"Image for {self.product.name}"


class WarehouseStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stocks', verbose_name="Product")
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stocks", verbose_name="Warehouse",default=1)
    quantity = models.PositiveIntegerField(verbose_name="Quantity")

    class Meta:
        verbose_name = "Warehouse Stock"
        verbose_name_plural = "Warehouse Stocks"
        unique_together = ('product', 'warehouse')  # Ensures that a product can only have one stock entry per warehouse

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units in {self.warehouse.name}"
