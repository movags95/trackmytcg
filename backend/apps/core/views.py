from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import ProtectedError
from .models import TCG, ProductType, Set, Product
from .serializers import TCGSerializer, ProductTypeSerializer, SetSerializer, ProductSerializer


class TCGViewSet(viewsets.ModelViewSet):
    """CRUD operations for TCGs"""
    queryset = TCG.objects.all()
    serializer_class = TCGSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "Cannot delete TCG that is referenced by other entities"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProductTypeViewSet(viewsets.ModelViewSet):
    """CRUD operations for Product Types"""
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "Cannot delete Product Type that is referenced by other entities"},
                status=status.HTTP_400_BAD_REQUEST
            )


class SetViewSet(viewsets.ModelViewSet):
    """CRUD operations for Sets"""
    queryset = Set.objects.all()
    serializer_class = SetSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tcg_id = self.request.query_params.get('tcg')
        if tcg_id:
            queryset = queryset.filter(tcg_id=tcg_id)
        return queryset

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "Cannot delete Set that is referenced by other entities"},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD operations for Products"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        tcg_id = self.request.query_params.get('tcg')
        set_id = self.request.query_params.get('set')
        product_type_id = self.request.query_params.get('product_type')

        if tcg_id:
            queryset = queryset.filter(tcg_id=tcg_id)
        if set_id:
            queryset = queryset.filter(set_id=set_id)
        if product_type_id:
            queryset = queryset.filter(product_type_id=product_type_id)

        return queryset

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError:
            return Response(
                {"error": "Cannot delete Product that is referenced by other entities"},
                status=status.HTTP_400_BAD_REQUEST
            )
