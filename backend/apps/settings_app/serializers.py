from rest_framework import serializers
from .models import UserSettings


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = [
            'user', 'currency', 'low_stock_threshold',
            'highlight_low_stock_color', 'highlight_out_stock_color',
            'default_date_range', 'default_time_aggregation'
        ]
        read_only_fields = ['user']
