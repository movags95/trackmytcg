from rest_framework import serializers
from .models import TCG, ProductType, Set, Product


class TCGSerializer(serializers.ModelSerializer):
    class Meta:
        model = TCG
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name', 'code', 'default_pack_count']
        read_only_fields = ['id']


class SetSerializer(serializers.ModelSerializer):
    tcg_name = serializers.CharField(source='tcg.name', read_only=True)

    class Meta:
        model = Set
        fields = ['id', 'tcg', 'tcg_name', 'name', 'code']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    tcg_name = serializers.CharField(source='tcg.name', read_only=True)
    set_name = serializers.CharField(source='set.name', read_only=True)
    product_type_name = serializers.CharField(source='product_type.name', read_only=True)
    product_type_code = serializers.CharField(source='product_type.code', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'tcg', 'tcg_name', 'set', 'set_name',
            'product_type', 'product_type_name', 'product_type_code',
            'name', 'pack_count', 'is_listed'
        ]
        read_only_fields = ['id']
