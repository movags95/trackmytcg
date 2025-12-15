from django.db import models
from django.contrib.auth.models import User


class UserSettings(models.Model):
    """User-specific settings"""
    CURRENCY_CHOICES = [
        ('GBP', 'GBP'),
        ('EUR', 'EUR'),
        ('USD', 'USD'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='settings')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='GBP')
    low_stock_threshold = models.IntegerField(default=5)
    highlight_low_stock_color = models.CharField(max_length=7, default='#FFA500')
    highlight_out_stock_color = models.CharField(max_length=7, default='#FF0000')
    default_date_range = models.CharField(max_length=50, default='30d')
    default_time_aggregation = models.CharField(max_length=50, default='daily')

    class Meta:
        db_table = 'user_settings'

    def __str__(self):
        return f"Settings for {self.user.username}"
