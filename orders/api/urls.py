from rest_framework.routers import DefaultRouter
from orders.api.views import PurchaseOrderViewSet, SalesOrderViewSet

router = DefaultRouter()
router.register(r'purchase-orders', PurchaseOrderViewSet, basename='purchase-order')
router.register(r'sales-orders', SalesOrderViewSet, basename='sales-order')

urlpatterns = router.urls

# Adding_Items 
#  purchase-orders/<int:pk>/add_items/ and sales-orders/<int:pk>/add_items/
#  sales-orders/<int:pk>/add_items/ and sales-orders/<int:pk>/add_items/


# Listing or Creating Purchase Order or Sales Order
#  purchase-orders/
#  sales-orders/

# Updating or Retiving Purchase Order or Sales Order
#  purchase-orders/<int:pk>/
#  sales-orders/<int:pk>/