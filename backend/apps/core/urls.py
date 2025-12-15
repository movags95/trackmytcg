from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TCGViewSet, ProductTypeViewSet, SetViewSet, ProductViewSet

router = DefaultRouter()
router.register(r'tcgs', TCGViewSet, basename='tcg')
router.register(r'product-types', ProductTypeViewSet, basename='product-type')
router.register(r'sets', SetViewSet, basename='set')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
