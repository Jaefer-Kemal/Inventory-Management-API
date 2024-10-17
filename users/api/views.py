from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from users.filters import UserFilter


from users.api.serializers import (
    EmployeeRegisterSerializer,
    SupplierRegisterSerializer,
    UserDetailSerializer,
    AddressSerializer,
    CustomerRegisterSerializer
    
)
from rest_framework import permissions
from rest_framework import generics
from users.models import CustomUser, Address


from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from users.api.serializers import EmployeeRegisterSerializer  # Import your serializer
from users.permissions import AddressPermission

# API View for registering employees (staff, store_manager)
class EmployeeRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    serializer_class = EmployeeRegisterSerializer

    def get(self, request, *args, **kwargs):
        return Response({"message": "Use the Access code given by Admin and Register"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# API View for registering suppliers
class SupplierRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    serializer_class = SupplierRegisterSerializer  # Specify the serializer

    def get(self, request, *args, **kwargs):
        return Response({"message": "Use the Access code given by Admin and Register"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs) 
    
    
class CustomerRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    serializer_class = CustomerRegisterSerializer  # Specify the serializer

    def get(self, request, *args, **kwargs):
        return Response({"message": "Use the Access code given by Admin and Register"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)   

# API View for retrieving user details
class UserDetailView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter 

  

# Api VIew for Address
class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter queryset to return only the address for the logged-in user
        return self.queryset.filter(user=self.request.user)
    
class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Check if the user already has an address
        if hasattr(request.user, 'address'):
            return Response({"detail": "Address already exists for this user."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the address with the user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)