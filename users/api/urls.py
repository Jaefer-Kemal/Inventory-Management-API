from django.urls import path
from users.api.views import EmployeeRegisterView, SupplierRegisterView, UserDetailView

urlpatterns = [
    path('register/employee/', EmployeeRegisterView.as_view(), name='employee-register'),
    path('register/supplier/', SupplierRegisterView.as_view(), name='supplier-register'),
    path('user/details/', UserDetailView.as_view(), name='user-details'),
]
