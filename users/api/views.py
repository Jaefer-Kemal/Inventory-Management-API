from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from users.filters import UserFilter
from django.urls import reverse

from users.api.serializers import (
    EmployeeRegisterSerializer,
    SupplierRegisterSerializer,
    UserDetailSerializer,
    AddressSerializer,
    CustomerRegisterSerializer,
    UserListSerializer,
    AcessCodeSerializer
)
from rest_framework import permissions
from rest_framework import generics
from users.models import CustomUser, Address, AcessCode


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
        return Response(
            {"message": "Use the Access code given by Admin and Register"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# API View for registering suppliers
class SupplierRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    serializer_class = SupplierRegisterSerializer  # Specify the serializer

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Use the Access code given by Admin and Register"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomerRegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]  # Allow registration for any user
    serializer_class = CustomerRegisterSerializer  # Specify the serializer

    def get(self, request, *args, **kwargs):
        return Response(
            {"message": "Use the Access code given by Admin and Register"},
            status=status.HTTP_200_OK,
        )

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# API View for retrieving user details
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter


class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def get_object(self):
        # Return the currently authenticated user
        return self.request.user

    def put(self, request, *args, **kwargs):
        # Fetch the user object (authenticated user)
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=False)  # Set partial=True if fields are optional

        if serializer.is_valid():
            serializer.save()  # Save the updated user details
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View to create address
class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        return Response({"message":"Create your own address"},status=status.HTTP_200_OK)
        
    def create(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"detail": "You need to be logged in to create an address."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Check if the user already has an address
        if hasattr(request.user, "address"):
            return Response(
                {"detail": "Address already exists for this user."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the address with the user
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for Address Details
class AddressDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def get_object(self):
        """
        Retrieve the user's address.
        """
        address = self.get_queryset().first()
        if address:
            return address
        else:
            # Return a 404 response if no address is found
            return None

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve the address of the authenticated user.
        """
        address = self.get_object()  # Retrieve the user's address
        if address is None:
            response_data = {
                            "result": {
                                "detail": "No address found for the current user.",
                                "solution": request.build_absolute_uri(reverse('address-create'))
                            }
                        }

            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        # Return the serialized address if found
        serializer = self.get_serializer(address)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Handle the update process for the user's address.
        """
        address = self.get_object()  # Retrieve the user's address

        # If no address is found, return a 404 response
        if address is None:
            response_data = {
                            "result": {
                                "detail": "No address found for the current user.",
                                "solution": request.build_absolute_uri(reverse('address-create'))
                            }
                        }

            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        # Proceed with the update if an address is found
        serializer = self.get_serializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Save the updated address
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class AccessCodeListCreateView(generics.ListCreateAPIView):
    queryset = AcessCode.objects.all()
    serializer_class = AcessCodeSerializer
    permission_classes = [IsAdminUser]

class AccessCodeDetailView(generics.RetrieveDestroyAPIView):
    queryset = AcessCode.objects.all()
    serializer_class = AcessCodeSerializer
    permission_classes = [IsAdminUser]
