from django.urls import path
from users.api.views import EmployeeRegisterView, SupplierRegisterView, UserDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/employee/', EmployeeRegisterView.as_view(), name='employee-register'),
    path('register/supplier/', SupplierRegisterView.as_view(), name='supplier-register'),
    path('list/', UserDetailView.as_view(), name='user-details'),
    
    
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    # Use the refresh token to get a new access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
