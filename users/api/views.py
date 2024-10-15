from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.api.serializers import (
    EmployeeRegisterSerializer,
    SupplierRegisterSerializer,
    UserDetailSerializer
)
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from users.models import CustomUser


# API View for registering employees (staff, store_manager)
class EmployeeRegisterView(APIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    def get(self, request, *args, **kwargs):
        return Response({"message":"Provide the Access code given by Admin and Register"},status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = EmployeeRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will call the 'create' method in the serializer
            return Response({"message": "Employee registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API View for registering suppliers
class SupplierRegisterView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        return Response({"message":"Provide the Access code given by Admin and Register"})

    def post(self, request, *args, **kwargs):
        serializer = SupplierRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will call the 'create' method in the serializer
            return Response({"message": "Supplier registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API View for retrieving user details
class UserDetailView(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserDetailSerializer

  
