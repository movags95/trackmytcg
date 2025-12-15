from decimal import Decimal
from django.db.models import Sum, F, Q, Count
from django.contrib.auth.models import User
from apps.core.models import Product
from apps.transactions.models import PurchaseLineItem, SaleLineItem, OpeningLineItem, Purchase


def get_inventory_for_user(user):
    """
    Calculate current inventory for all products for a given user.
    Per PRD Section 1.9.2: inventory_quantity = received_purchases − sold_quantity − opened_quantity

    Returns a list of dictionaries with product inventory and derived metrics.
    """
    products = Product.objects.all()
    inventory_data = []

    for product in products:
        # Calculate received purchases (only where purchase status = RECEIVED)
        received = PurchaseLineItem.objects.filter(
            product=product,
            purchase__user=user,
            purchase__status='RECEIVED'
        ).aggregate(total=Sum('quantity'))['total'] or 0

        # Calculate sold quantity
        sold = SaleLineItem.objects.filter(
            product=product,
            sale__user=user
        ).aggregate(total=Sum('quantity'))['total'] or 0

        # Calculate opened quantity
        opened = OpeningLineItem.objects.filter(
            product=product,
            opening__user=user
        ).aggregate(total=Sum('quantity'))['total'] or 0

        # Calculate current inventory
        current_quantity = received - sold - opened

        # Only include products with inventory > 0 or products that have history
        if current_quantity > 0 or sold > 0 or opened > 0:
            # Calculate average unit cost
            avg_cost = calculate_average_unit_cost(product, user)

            # Calculate average ROI
            avg_roi = calculate_average_roi(product, user)

            # Get last sale price
            last_sale_price = get_last_sale_price(product, user)

            # Calculate price per pack
            price_per_pack = None
            if avg_cost and product.pack_count:
                price_per_pack = avg_cost / product.pack_count

            inventory_data.append({
                'product': product,
                'product_id': str(product.id),
                'product_name': product.name,
                'tcg': product.tcg.name,
                'set': product.set.name,
                'product_type': product.product_type.name,
                'quantity': current_quantity,
                'average_cost': float(avg_cost) if avg_cost else None,
                'average_roi': float(avg_roi) if avg_roi else None,
                'price_per_pack': float(price_per_pack) if price_per_pack else None,
                'is_listed': product.is_listed,
                'last_sale_price': float(last_sale_price) if last_sale_price else None,
                'pack_count': product.pack_count,
            })

    return inventory_data


def calculate_average_unit_cost(product, user):
    """
    Calculate average unit cost for a product including proportional delivery fee allocation.
    Per PRD Section 1.9.3:
    average_unit_cost = total_received_cost ÷ total_received_quantity
    Delivery fee allocation is proportional to line item cost within the purchase.
    """
    # Get all received purchase line items for this product
    line_items = PurchaseLineItem.objects.filter(
        product=product,
        purchase__user=user,
        purchase__status='RECEIVED'
    ).select_related('purchase')

    if not line_items.exists():
        return None

    total_cost_with_delivery = Decimal('0.00')
    total_quantity = 0

    for item in line_items:
        # Line item cost
        line_item_cost = item.quantity * item.unit_cost

        # Get purchase total (sum of all line items in this purchase)
        purchase_total = sum(
            li.quantity * li.unit_cost
            for li in item.purchase.line_items.all()
        )

        # Calculate proportional delivery fee for this line item
        if purchase_total > 0:
            delivery_fee_proportion = (line_item_cost / purchase_total) * item.purchase.delivery_fee
        else:
            delivery_fee_proportion = Decimal('0.00')

        # Add to totals
        total_cost_with_delivery += line_item_cost + delivery_fee_proportion
        total_quantity += item.quantity

    if total_quantity > 0:
        return total_cost_with_delivery / total_quantity
    return None


def calculate_average_roi(product, user):
    """
    Calculate average ROI for sold items of this product.
    Per PRD Section 1.9.6: ROI = (profit ÷ COGS) × 100
    """
    sale_items = SaleLineItem.objects.filter(
        product=product,
        sale__user=user
    ).select_related('sale')

    if not sale_items.exists():
        return None

    avg_cost = calculate_average_unit_cost(product, user)
    if not avg_cost:
        return None

    total_profit = Decimal('0.00')
    total_cogs = Decimal('0.00')

    for sale_item in sale_items:
        # Calculate COGS for this sale item
        cogs = sale_item.quantity * avg_cost

        # Calculate gross revenue for this sale item
        gross_revenue = sale_item.quantity * sale_item.unit_sale_price

        # Calculate proportional costs for this sale item
        # Get total gross revenue for the entire sale
        sale_gross_total = sum(
            si.quantity * si.unit_sale_price
            for si in sale_item.sale.line_items.all()
        )

        if sale_gross_total > 0:
            # Proportional allocation of shipping, fees, and tax
            proportion = gross_revenue / sale_gross_total
            allocated_shipping = sale_item.sale.shipping_cost * proportion
            allocated_fees = sale_item.sale.platform_fees * proportion
            allocated_tax = sale_item.sale.tax * proportion
        else:
            allocated_shipping = allocated_fees = allocated_tax = Decimal('0.00')

        # Calculate net revenue for this sale item
        net_revenue = gross_revenue - allocated_shipping - allocated_fees - allocated_tax

        # Calculate profit
        profit = net_revenue - cogs

        total_profit += profit
        total_cogs += cogs

    if total_cogs > 0:
        roi = (total_profit / total_cogs) * 100
        return roi
    return None


def get_last_sale_price(product, user):
    """
    Get the average unit sale price from the most recent sale of this product.
    Used for unrealized inventory valuation per PRD Section 1.9.8.
    """
    last_sale_item = SaleLineItem.objects.filter(
        product=product,
        sale__user=user
    ).select_related('sale').order_by('-sale__sale_date').first()

    if last_sale_item:
        return last_sale_item.unit_sale_price
    return None


def get_unrealized_inventory_value(user):
    """
    Calculate total unrealized inventory value for all products.
    Per PRD Section 1.9.8:
    unrealized_value = inventory_quantity × average_unit_sale_price
    If no sales exist for a product, unrealized value = 0 and flagged as "No market data"
    """
    inventory = get_inventory_for_user(user)
    total_unrealized_value = Decimal('0.00')

    for item in inventory:
        if item['quantity'] > 0:
            if item['last_sale_price']:
                unrealized_value = item['quantity'] * Decimal(str(item['last_sale_price']))
                total_unrealized_value += unrealized_value
            # If no last_sale_price, it's flagged as "No market data" and contributes 0

    return float(total_unrealized_value)
