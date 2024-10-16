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


urlpatterns = [
    path("api-auth/", include("rest_framework.urls")),
    path('admin/', admin.site.urls),  # Admin site URL
    path('api/auditlog/', include('auditlog.api.urls')),  # Include auditlog app URLs
    path('api/inventory/', include('inventory.api.urls')),  # Include inventory app URLs
    path('api/orders/', include('orders.api.urls')),  # Include orders app URLs
    path('api/account/', include('users.api.urls')),  # Include users app URLs
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)