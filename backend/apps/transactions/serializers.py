from rest_framework import serializers
from .models import Purchase, PurchaseLineItem, Sale, SaleLineItem, Opening, OpeningLineItem
from apps.core.serializers import ProductSerializer


class PurchaseLineItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = PurchaseLineItem
        fields = ['id', 'product', 'product_details', 'quantity', 'unit_cost']
        read_only_fields = ['id']


class PurchaseSerializer(serializers.ModelSerializer):
    line_items = PurchaseLineItemSerializer(many=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = Purchase
        fields = [
            'id', 'user', 'purchase_date', 'vendor', 'online_order',
            'delivery_fee', 'status', 'notes', 'line_items', 'total_cost',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_total_cost(self, obj):
        """Calculate total purchase cost: sum of line items + delivery fee"""
        line_items_total = sum(
            item.quantity * item.unit_cost for item in obj.line_items.all()
        )
        return line_items_total + obj.delivery_fee

    def create(self, validated_data):
        line_items_data = validated_data.pop('line_items')
        # Get the hardcoded user (id=1)
        from django.contrib.auth.models import User
        user = User.objects.first()
        purchase = Purchase.objects.create(user=user, **validated_data)

        for line_item_data in line_items_data:
            PurchaseLineItem.objects.create(purchase=purchase, **line_item_data)

        return purchase

    def update(self, instance, validated_data):
        line_items_data = validated_data.pop('line_items', None)

        # Update purchase fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update line items if provided
        if line_items_data is not None:
            instance.line_items.all().delete()
            for line_item_data in line_items_data:
                PurchaseLineItem.objects.create(purchase=instance, **line_item_data)

        return instance


class SaleLineItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = SaleLineItem
        fields = ['id', 'product', 'product_details', 'quantity', 'unit_sale_price']
        read_only_fields = ['id']


class SaleSerializer(serializers.ModelSerializer):
    line_items = SaleLineItemSerializer(many=True)
    gross_revenue = serializers.SerializerMethodField()
    net_revenue = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = [
            'id', 'user', 'sale_date', 'platform', 'shipping_paid_by',
            'shipping_cost', 'platform_fees', 'tax', 'sale_url', 'buyer_username',
            'line_items', 'gross_revenue', 'net_revenue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_gross_revenue(self, obj):
        """Calculate gross revenue: sum of (quantity × unit_sale_price)"""
        return sum(
            item.quantity * item.unit_sale_price for item in obj.line_items.all()
        )

    def get_net_revenue(self, obj):
        """Calculate net revenue: gross revenue - shipping - platform_fees - tax"""
        gross = self.get_gross_revenue(obj)
        return gross - obj.shipping_cost - obj.platform_fees - obj.tax

    def create(self, validated_data):
        line_items_data = validated_data.pop('line_items')
        # Get the hardcoded user (id=1)
        from django.contrib.auth.models import User
        user = User.objects.first()
        sale = Sale.objects.create(user=user, **validated_data)

        for line_item_data in line_items_data:
            SaleLineItem.objects.create(sale=sale, **line_item_data)

        return sale

    def update(self, instance, validated_data):
        line_items_data = validated_data.pop('line_items', None)

        # Update sale fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update line items if provided
        if line_items_data is not None:
            instance.line_items.all().delete()
            for line_item_data in line_items_data:
                SaleLineItem.objects.create(sale=instance, **line_item_data)

        return instance


class OpeningLineItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OpeningLineItem
        fields = ['id', 'product', 'product_details', 'quantity']
        read_only_fields = ['id']


class OpeningSerializer(serializers.ModelSerializer):
    line_items = OpeningLineItemSerializer(many=True)

    class Meta:
        model = Opening
        fields = ['id', 'user', 'opened_date', 'line_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def create(self, validated_data):
        line_items_data = validated_data.pop('line_items')
        # Get the hardcoded user (id=1)
        from django.contrib.auth.models import User
        user = User.objects.first()
        opening = Opening.objects.create(user=user, **validated_data)

        for line_item_data in line_items_data:
            OpeningLineItem.objects.create(opening=opening, **line_item_data)

        return opening

    def update(self, instance, validated_data):
        line_items_data = validated_data.pop('line_items', None)

        # Update opening fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update line items if provided
        if line_items_data is not None:
            instance.line_items.all().delete()
            for line_item_data in line_items_data:
                OpeningLineItem.objects.create(opening=instance, **line_item_data)

        return instance
