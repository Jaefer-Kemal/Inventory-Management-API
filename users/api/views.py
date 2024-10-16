from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from users.filters import UserFilter


from users.api.serializers import (
    EmployeeRegisterSerializer,
    SupplierRegisterSerializer,
    UserDetailSerializer
)
from rest_framework.permissions import AllowAny
from rest_framework import generics
from users.models import CustomUser


# API View for registering employees (staff, store_manager)
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from .serializers import EmployeeRegisterSerializer  # Import your serializer

class EmployeeRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    serializer_class = EmployeeRegisterSerializer

    def get(self, request, *args, **kwargs):
        return Response({"message": "Provide the Access code given by Admin and Register"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# API View for registering suppliers
class SupplierRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    serializer_class = SupplierRegisterSerializer  # Specify the serializer

    def get(self, request, *args, **kwargs):
        return Response({"message": "Provide the Access code given by Admin and Register"}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs) 
    
# API View for retrieving user details
class UserDetailView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter 

  
