from rest_framework import serializers
from users.models import CustomUser, Supplier, Address, AcessCode


# Serializer for registering employees (staff, store_manager)
class EmployeeRegisterSerializer(serializers.ModelSerializer):
    access_code = serializers.CharField(write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    role = serializers.ReadOnlyField()
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password2",
            "role",
            "access_code",
        ]
        extra_kwargs = {
            "password": {"write_only": True}  # Set password to be write-only for security
        }

    def validate(self, data):
        access_code_value = data.get("access_code")
        try:
            # Check if the access code exists and if it matches the role
            access_code = AcessCode.objects.get(code=access_code_value)
        except AcessCode.DoesNotExist:
            raise serializers.ValidationError("Invalid access code.")

        if access_code.role not in ["staff", "store_manager"]:
            raise serializers.ValidationError(
                "Access code does not match employee roles."
            )

        # If access code role is 'staff', set necessary flags
        if access_code.role == "staff":
            data["is_staff"] = True
            data["is_verified"] = True
            data["role"] = "staff"
        # If access code role is 'store_manager', set necessary flags
        elif access_code.role == "store_manager":
            data["is_verified"] = True
            data["role"] = "store_manager"
        return data

    def create(self, validated_data):
        # Remove access code from the data
        validated_data.pop("access_code", None)
        password = validated_data.pop("password", None)
        password2 = validated_data.pop("password2", None)
         # Check if both passwords match
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        
        user = CustomUser.objects.create(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


# Serializer for registering suppliers
class SupplierRegisterSerializer(serializers.ModelSerializer):
    access_code = serializers.CharField(write_only=True)
    company_name = serializers.CharField(max_length=255, write_only=True)
    phone_number = serializers.CharField(max_length=15, write_only=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)
    supplier_company_name = serializers.SerializerMethodField()
    supplier_phone_number = serializers.SerializerMethodField()
    role = serializers.ReadOnlyField()
    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "password2",
            "access_code",
            "company_name",
            "phone_number",
            "role",
            "supplier_company_name",
            "supplier_phone_number"
        ]
        extra_kwargs = {
            "password": {"write_only": True}  # Set password to be write-only for security
        }
    def validate(self, data):
        access_code_value = data.get("access_code")
        try:
            # Check if the access code exists and if it matches the supplier role
            access_code = AcessCode.objects.get(code=access_code_value)
        except AcessCode.DoesNotExist:
            raise serializers.ValidationError("Invalid access code.")

        if access_code.role != "supplier":
            raise serializers.ValidationError(
                "Access code does not match supplier role."
            )

        # Set necessary flags for suppliers
        data["is_verified"] = True
        data["role"] = "supplier"
        return data
 
    def create(self, validated_data):
        # Remove access code and supplier specific fields from validated_data
        access_code_value = validated_data.pop("access_code", None)
        company_name = validated_data.pop("company_name", None)
        phone_number = validated_data.pop("phone_number", None)
        
        password2 = validated_data.pop("password2", None)
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create(**validated_data)
        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        
        if password:
            user.set_password(password)
        user.save()

        # Create the Supplier model after the user is created
        Supplier.objects.create(
            user=user, company_name=company_name, phone_number=phone_number
        )

        return user

    def get_supplier_company_name(self,obj):
        company_name = obj.supplier_profile.company_name
        return company_name
    def get_supplier_phone_number(self,obj):
        phone_number = obj.supplier_profile.phone_number
        return phone_number

# Serializer for user addresses
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "city", "state", "postal_code", "country"]


# Serializer for user details with address
class UserDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "role",
            "is_verified",
            "address",
        ]
