from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .calculations import get_inventory_for_user, get_unrealized_inventory_value


class InventoryView(APIView):
    """
    GET endpoint to retrieve current inventory with calculated metrics.
    Supports search and filtering.
    """

    def get(self, request):
        user = User.objects.first()  # Hardcoded user
        inventory = get_inventory_for_user(user)

        # Apply search filter
        search = request.query_params.get('search')
        if search:
            inventory = [
                item for item in inventory
                if search.lower() in item['product_name'].lower()
                or search.lower() in item['tcg'].lower()
                or search.lower() in item['set'].lower()
            ]

        # Filter by TCG
        tcg_filter = request.query_params.get('tcg')
        if tcg_filter:
            inventory = [item for item in inventory if item['tcg'] == tcg_filter]

        # Filter by stock status
        stock_status = request.query_params.get('stock_status')
        if stock_status == 'in_stock':
            inventory = [item for item in inventory if item['quantity'] > 0]
        elif stock_status == 'out_of_stock':
            inventory = [item for item in inventory if item['quantity'] == 0]

        # Filter by listed status
        is_listed = request.query_params.get('is_listed')
        if is_listed is not None:
            is_listed_bool = is_listed.lower() == 'true'
            inventory = [item for item in inventory if item['is_listed'] == is_listed_bool]

        return Response({
            'inventory': inventory,
            'total_items': len(inventory),
            'total_unrealized_value': get_unrealized_inventory_value(user)
        })


class InventoryValueView(APIView):
    """
    GET endpoint to retrieve total unrealized inventory value.
    """

    def get(self, request):
        user = User.objects.first()  # Hardcoded user
        total_value = get_unrealized_inventory_value(user)

        return Response({
            'unrealized_inventory_value': total_value
        })
