from django.test import TestCase
from django.contrib.auth import get_user_model
from users.models import Supplier, Customer, UserRank, Address, AcessCode

CustomUser = get_user_model()

class CustomUserModelTest(TestCase):
    def setUp(self):
        # Set up a default user
        self.user = CustomUser.objects.create_user(
            email="testuser@example.com",
            username="testuser",
            password="password123",
            role="customer"
        )
    
    def test_user_creation(self):
        user = CustomUser.objects.get(email="testuser@example.com")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.check_password("password123"))

    def test_superuser_creation(self):
        admin_user = CustomUser.objects.create_superuser(
            email="admin@example.com",
            username="admin",
            password="adminpassword123"
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)
        self.assertEqual(admin_user.role, 'admin')

    def test_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            CustomUser.objects.create_user(
                email="",
                password="password123"
            )


class SupplierModelTest(TestCase):
    def setUp(self):
        # Create a user and associate them with a supplier profile
        self.supplier_user = CustomUser.objects.create_user(
            email="supplier@example.com",
            username="supplieruser",
            password="password123",
            role="supplier"
        )
    
    def test_supplier_profile_creation(self):
        supplier = Supplier.objects.create(
            user=self.supplier_user,
            company_name="Supplier Company",
            phone_number="123456789"
        )
        self.assertEqual(supplier.user.email, "supplier@example.com")
        self.assertEqual(supplier.company_name, "Supplier Company")
    
    def test_supplier_default_rank(self):
        supplier = Supplier.objects.create(
            user=self.supplier_user,
            company_name="Supplier Company",
            phone_number="123456789"
        )
        self.assertTrue(supplier.rank.filter(rank="bronze").exists())


class CustomerModelTest(TestCase):
    def setUp(self):
        # Create a user and associate them with a customer profile
        self.customer_user = CustomUser.objects.create_user(
            email="customer@example.com",
            username="customeruser",
            password="password123",
            role="customer"
        )

    def test_customer_profile_creation(self):
        customer = Customer.objects.create(
            user=self.customer_user,
            phone_number="987654321"
        )
        self.assertEqual(customer.user.email, "customer@example.com")
        self.assertEqual(customer.phone_number, "987654321")

    def test_customer_default_rank(self):
        customer = Customer.objects.create(
            user=self.customer_user,
            phone_number="987654321"
        )
        self.assertTrue(customer.rank.filter(rank="bronze").exists())


class AddressModelTest(TestCase):
    def setUp(self):
        # Create a user and associate an address with the user
        self.user = CustomUser.objects.create_user(
            email="user@example.com",
            username="testuser",
            password="password123"
        )

    def test_address_creation(self):
        address = Address.objects.create(
            user=self.user,
            country="Ethiopia",
            street="123 Test Street",
            city="Adama",
            state="Oromia",
            postal_code="12345"
        )
        self.assertEqual(address.user.email, "user@example.com")
        self.assertEqual(address.city, "Adama")


class AcessCodeModelTest(TestCase):
    def test_access_code_creation(self):
        access_code = AcessCode.objects.create(
            code="XYZ123",
            role="customer"
        )
        self.assertEqual(access_code.code, "XYZ123")
        self.assertEqual(access_code.role, "customer")
