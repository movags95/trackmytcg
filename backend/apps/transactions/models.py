import uuid
from django.db import models
from django.contrib.auth.models import User
from apps.core.models import Product


class Purchase(models.Model):
    """Purchase transaction header"""
    STATUS_CHOICES = [
        ('PREORDER', 'Preorder'),
        ('AWAITING', 'Awaiting Delivery'),
        ('RECEIVED', 'Received'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    purchase_date = models.DateField()
    vendor = models.CharField(max_length=255)
    online_order = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='RECEIVED')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'purchases'
        ordering = ['-purchase_date', '-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['purchase_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Purchase {self.purchase_date} - {self.vendor}"


class PurchaseLineItem(models.Model):
    """Purchase line items"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='line_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='purchase_items')
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'purchase_line_items'
        indexes = [
            models.Index(fields=['purchase']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.product} x{self.quantity}"


class Sale(models.Model):
    """Sales transaction header"""
    SHIPPING_PAID_BY_CHOICES = [
        ('BUYER', 'Buyer'),
        ('SELLER', 'Seller'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')
    sale_date = models.DateField()
    platform = models.CharField(max_length=255)
    shipping_paid_by = models.CharField(max_length=10, choices=SHIPPING_PAID_BY_CHOICES)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    platform_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sale_url = models.URLField(blank=True, null=True)
    buyer_username = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'sales'
        ordering = ['-sale_date', '-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['sale_date']),
        ]

    def __str__(self):
        return f"Sale {self.sale_date} - {self.platform}"


class SaleLineItem(models.Model):
    """Sale line items"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='line_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sale_items')
    quantity = models.IntegerField()
    unit_sale_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'sale_line_items'
        indexes = [
            models.Index(fields=['sale']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.product} x{self.quantity}"


class Opening(models.Model):
    """Personal use opening transaction header"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='openings')
    opened_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'openings'
        ordering = ['-opened_date', '-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['opened_date']),
        ]

    def __str__(self):
        return f"Opening {self.opened_date}"


class OpeningLineItem(models.Model):
    """Opening line items"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    opening = models.ForeignKey(Opening, on_delete=models.CASCADE, related_name='line_items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='opening_items')
    quantity = models.IntegerField()

    class Meta:
        db_table = 'opening_line_items'
        indexes = [
            models.Index(fields=['opening']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.product} x{self.quantity}"
