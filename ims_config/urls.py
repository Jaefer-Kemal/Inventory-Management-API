"""
URL configuration for ims_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, re_path

schema_view = get_schema_view(
    openapi.Info(
        title="Inventory Management API",
        default_version='v1',
        description="API documentation for the Inventory Management System",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="jaeferkemal@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path('admin/', admin.site.urls,name="admin"),  # Admin site URL
    path('api/auditlog/', include('auditlog.api.urls')),  # Include auditlog app URLs
    path('api/inventory/', include('inventory.api.urls')),  # Include inventory app URLs
    path('api/orders/', include('orders.api.urls')),  # Include orders app URLs
    path('api/account/', include('users.api.urls')),  # Include users app URLs
    path('api/warehouse/', include('warehouse.api.urls')),  # Include warehouse app URLs
    path('', include('home.urls')),
    # Swagger UI:
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # ReDoc UI:
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)