from django.db import models
from cloudinary.models import CloudinaryField
from cloudinary.uploader import destroy


class Warehouse(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=20, null=True, blank=True)
    # image = models.ImageField(upload_to="warehouse/", blank=True, null=True) 
    image = CloudinaryField('image', folder='warehouse/', blank=True, null=True) # Organized field options
    created_at = models.DateTimeField(auto_now_add=True)  # Add created date
    updated_at = models.DateTimeField(auto_now=True)  # Auto-updating timestamp on change

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'
        ordering = ['name']  # Default ordering by name

    def __str__(self):
        return f"Warehouse: {self.name} - {self.city or 'No City'}, {self.country}"

    @property
    def full_address(self):
        """Returns the full address of the warehouse in a single string."""
        address_parts = filter(None, [self.address, self.city, self.state, self.postal_code, self.country])
        return ', '.join(address_parts)
    
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
