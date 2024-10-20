from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from uuid import uuid4

class UserRank(models.Model):
    RANKING = [
        ("bronze", "Bronze"),
        ("silver", "Silver"),
        ("gold", "Gold"),
        ("platinum", "Platinum"),  
    ]
    rank = models.CharField(max_length=15, choices=RANKING, unique=True) 

    def __str__(self):
        return self.rank

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_verified', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
    ('staff', 'Staff'),
    ('store_manager', 'Store Manager'),
    ('supplier', 'Supplier'),
    ("customer","Customer")
]


    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)  
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ["username"]  

    def __str__(self):
        return f"{self.username} ({self.email})"
    
    class Meta:
        verbose_name = "User"
    
    
class Supplier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='supplier_profile')
    company_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    rank = models.ManyToManyField(UserRank,related_name="suppliers_with_rank")
    def __str__(self):
        return f"{self.user.username}|{self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        if not self.rank.exists():
            bronze_rank, created = UserRank.objects.get_or_create(rank="bronze")
            self.rank.add(bronze_rank)
    
    
    
    
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    phone_number = models.CharField(max_length=15)
    rank = models.ManyToManyField(UserRank,related_name="customers_with_rank")
    def __str__(self):
        return f"{self.user.username}|{self.id}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
        if not self.rank.exists():
            bronze_rank, created = UserRank.objects.get_or_create(rank="bronze")
            self.rank.add(bronze_rank)
    
class Address(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='address')
    country = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=255, blank=True,null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Address"
    
class AcessCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    code = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=CustomUser.ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.id} {self.role}"
    
    
