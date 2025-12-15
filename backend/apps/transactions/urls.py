from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PurchaseViewSet, SaleViewSet, OpeningViewSet

router = DefaultRouter()
router.register(r'purchases', PurchaseViewSet, basename='purchase')
router.register(r'sales', SaleViewSet, basename='sale')
router.register(r'openings', OpeningViewSet, basename='opening')

urlpatterns = [
    path('', include(router.urls)),
]
