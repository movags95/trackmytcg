import uuid
from django.db import models


class TCG(models.Model):
    """Trading Card Game master data"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'tcgs'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """Product type master data (e.g., Booster Box, Elite Trainer Box)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10)
    default_pack_count = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'product_types'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class Set(models.Model):
    """TCG set master data"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tcg = models.ForeignKey(TCG, on_delete=models.PROTECT, related_name='sets')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50)

    class Meta:
        db_table = 'sets'
        ordering = ['tcg', 'name']
        indexes = [
            models.Index(fields=['tcg']),
        ]

    def __str__(self):
        return f"{self.tcg.name} - {self.name}"


class Product(models.Model):
    """Sealed product master data"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tcg = models.ForeignKey(TCG, on_delete=models.PROTECT, related_name='products')
    set = models.ForeignKey(Set, on_delete=models.PROTECT, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products')
    name = models.CharField(max_length=255)
    pack_count = models.IntegerField()
    is_listed = models.BooleanField(default=False)

    class Meta:
        db_table = 'products'
        ordering = ['tcg', 'set', 'product_type']
        indexes = [
            models.Index(fields=['tcg']),
            models.Index(fields=['set']),
            models.Index(fields=['product_type']),
        ]

    def __str__(self):
        return f"{self.tcg.name} - {self.set.name} - {self.product_type.name}"
