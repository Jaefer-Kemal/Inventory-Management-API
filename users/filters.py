import django_filters
from .models import CustomUser

class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')  # Case-insensitive contains
    username = django_filters.CharFilter(lookup_expr='icontains')  # Case-insensitive contains
    role = django_filters.CharFilter()  # Exact match
    is_verified = django_filters.BooleanFilter()  # Boolean filter for true/false

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'role', 'is_verified']