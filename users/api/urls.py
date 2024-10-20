from django.urls import path
from users.api.views import (EmployeeRegisterView, 
                             SupplierRegisterView, 
                             UserDetailView, 
                             AddressCreateView, 
                             CustomerRegisterView,
                             UserDetailView, 
                             UserListView, 
                             AddressDetailView,
                             AccessCodeDetailView,
                             AccessCodeListCreateView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/employee/', EmployeeRegisterView.as_view(), name='employee-register'),
    path('register/supplier/', SupplierRegisterView.as_view(), name='supplier-register'),
    path('register/customer/', CustomerRegisterView.as_view(), name='customer-register'),
    path('list/', UserListView.as_view(), name='user-details'),
    
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Use the refresh token to get a new access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

     path('user/', UserDetailView.as_view(), name='user-detail'),  # View user details with address
    path('user/address-create/', AddressCreateView.as_view(), name='address-create'),  # Create user address
    path('user/address/', AddressDetailView.as_view(), name='address-detail'), 
    
     path('access-codes/', AccessCodeListCreateView.as_view(), name='access_code_list_create'),
    path('access-codes/<uuid:pk>/', AccessCodeDetailView.as_view(), name='access_code_detail'),
]