from django.urls import path
from .views import InventoryView, InventoryValueView

urlpatterns = [
    path('', InventoryView.as_view(), name='inventory'),
    path('value/', InventoryValueView.as_view(), name='inventory-value'),
]
