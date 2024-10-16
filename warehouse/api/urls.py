# urls.py

from django.urls import path
from warehouse.api.views import WarehouseProductsView, WarehouseDetailView, WarehouseListView

urlpatterns = [
    path("/",WarehouseListView.as_view(),name = "warehouse-list"),
    path("<int:pk>",WarehouseDetailView.as_view(),name = "warehouse-detail"),
    path("<int:pk>/products/", WarehouseProductsView.as_view(), name="warehouse-products"),
]
