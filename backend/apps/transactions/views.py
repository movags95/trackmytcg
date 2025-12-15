from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Purchase, Sale, Opening
from .serializers import PurchaseSerializer, SaleSerializer, OpeningSerializer


class PurchaseViewSet(viewsets.ModelViewSet):
    """CRUD operations for Purchases"""
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        user = User.objects.first()  # Hardcoded user
        queryset = Purchase.objects.filter(user=user)

        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(purchase_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(purchase_date__lte=end_date)

        return queryset


class SaleViewSet(viewsets.ModelViewSet):
    """CRUD operations for Sales"""
    serializer_class = SaleSerializer

    def get_queryset(self):
        user = User.objects.first()  # Hardcoded user
        queryset = Sale.objects.filter(user=user)

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(sale_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(sale_date__lte=end_date)

        # Filter by platform
        platform = self.request.query_params.get('platform')
        if platform:
            queryset = queryset.filter(platform__icontains=platform)

        return queryset


class OpeningViewSet(viewsets.ModelViewSet):
    """CRUD operations for Openings"""
    serializer_class = OpeningSerializer

    def get_queryset(self):
        user = User.objects.first()  # Hardcoded user
        queryset = Opening.objects.filter(user=user)

        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(opened_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(opened_date__lte=end_date)

        return queryset
