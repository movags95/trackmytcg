from decimal import Decimal
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from apps.transactions.models import Purchase, Sale, Opening, SaleLineItem, PurchaseLineItem
from apps.inventory.calculations import calculate_average_unit_cost, get_unrealized_inventory_value


def get_total_invested(user, start_date=None, end_date=None):
    """
    Calculate total amount invested in purchases.
    Per PRD Section 1.9.1: purchase_total_cost = Σ(line_item_cost) + delivery_fee
    Only count received purchases.
    """
    purchases = Purchase.objects.filter(user=user, status='RECEIVED')

    if start_date:
        purchases = purchases.filter(purchase_date__gte=start_date)
    if end_date:
        purchases = purchases.filter(purchase_date__lte=end_date)

    total = Decimal('0.00')
    for purchase in purchases:
        # Sum of line items
        line_items_total = sum(
            item.quantity * item.unit_cost
            for item in purchase.line_items.all()
        )
        # Add delivery fee
        total += line_items_total + purchase.delivery_fee

    return float(total)


def get_total_realized_profit(user, start_date=None, end_date=None):
    """
    Calculate total profit from sales.
    Per PRD Section 1.9.5: profit = net_revenue − COGS
    where net_revenue = gross_revenue − shipping − platform_fees − tax
    and COGS = quantity_sold × average_unit_cost
    """
    sales = Sale.objects.filter(user=user)

    if start_date:
        sales = sales.filter(sale_date__gte=start_date)
    if end_date:
        sales = sales.filter(sale_date__lte=end_date)

    total_profit = Decimal('0.00')

    for sale in sales:
        # Calculate gross revenue
        gross_revenue = sum(
            item.quantity * item.unit_sale_price
            for item in sale.line_items.all()
        )

        # Calculate net revenue
        net_revenue = gross_revenue - sale.shipping_cost - sale.platform_fees - sale.tax

        # Calculate COGS for all items in this sale
        cogs = Decimal('0.00')
        for item in sale.line_items.all():
            avg_cost = calculate_average_unit_cost(item.product, user)
            if avg_cost:
                cogs += item.quantity * avg_cost

        # Calculate profit
        profit = net_revenue - cogs
        total_profit += profit

    return float(total_profit)


def get_break_even_revenue(user):
    """
    Per PRD Section 1.9.9:
    break_even = total_invested − total_realized_profit
    If value ≤ 0, portfolio is considered break-even or profitable.
    """
    total_invested = Decimal(str(get_total_invested(user)))
    total_profit = Decimal(str(get_total_realized_profit(user)))

    break_even = total_invested - total_profit
    return float(break_even)


def get_average_profit_per_sale(user, start_date=None, end_date=None):
    """
    Calculate average profit per sale transaction.
    """
    sales = Sale.objects.filter(user=user)

    if start_date:
        sales = sales.filter(sale_date__gte=start_date)
    if end_date:
        sales = sales.filter(sale_date__lte=end_date)

    if not sales.exists():
        return 0.0

    total_profit = Decimal(str(get_total_realized_profit(user, start_date, end_date)))
    num_sales = sales.count()

    return float(total_profit / num_sales) if num_sales > 0 else 0.0


def get_cost_breakdown(user, start_date=None, end_date=None):
    """
    Breakdown of shipping, platform fees, and tax.
    """
    sales = Sale.objects.filter(user=user)

    if start_date:
        sales = sales.filter(sale_date__gte=start_date)
    if end_date:
        sales = sales.filter(sale_date__lte=end_date)

    total_shipping = sales.aggregate(total=Sum('shipping_cost'))['total'] or Decimal('0.00')
    total_fees = sales.aggregate(total=Sum('platform_fees'))['total'] or Decimal('0.00')
    total_tax = sales.aggregate(total=Sum('tax'))['total'] or Decimal('0.00')

    return {
        'shipping': float(total_shipping),
        'platform_fees': float(total_fees),
        'tax': float(total_tax),
        'total': float(total_shipping + total_fees + total_tax)
    }


def get_profit_by_tcg(user, start_date=None, end_date=None):
    """
    Calculate profit breakdown by TCG.
    """
    sales = Sale.objects.filter(user=user)

    if start_date:
        sales = sales.filter(sale_date__gte=start_date)
    if end_date:
        sales = sales.filter(sale_date__lte=end_date)

    tcg_profits = {}

    for sale in sales:
        for item in sale.line_items.all():
            tcg_name = item.product.tcg.name

            # Calculate item revenue
            item_gross = item.quantity * item.unit_sale_price

            # Calculate proportional costs
            sale_gross_total = sum(
                si.quantity * si.unit_sale_price
                for si in sale.line_items.all()
            )

            if sale_gross_total > 0:
                proportion = item_gross / sale_gross_total
                allocated_shipping = sale.shipping_cost * proportion
                allocated_fees = sale.platform_fees * proportion
                allocated_tax = sale.tax * proportion
            else:
                allocated_shipping = allocated_fees = allocated_tax = Decimal('0.00')

            item_net = item_gross - allocated_shipping - allocated_fees - allocated_tax

            # Calculate COGS
            avg_cost = calculate_average_unit_cost(item.product, user)
            cogs = item.quantity * avg_cost if avg_cost else Decimal('0.00')

            # Calculate profit
            profit = item_net - cogs

            if tcg_name not in tcg_profits:
                tcg_profits[tcg_name] = Decimal('0.00')
            tcg_profits[tcg_name] += profit

    return [
        {'tcg': tcg, 'profit': float(profit)}
        for tcg, profit in sorted(tcg_profits.items(), key=lambda x: x[1], reverse=True)
    ]


def get_profit_by_set(user, start_date=None, end_date=None):
    """
    Calculate profit breakdown by Set.
    """
    sales = Sale.objects.filter(user=user)

    if start_date:
        sales = sales.filter(sale_date__gte=start_date)
    if end_date:
        sales = sales.filter(sale_date__lte=end_date)

    set_profits = {}

    for sale in sales:
        for item in sale.line_items.all():
            set_name = f"{item.product.tcg.name} - {item.product.set.name}"

            # Calculate item revenue
            item_gross = item.quantity * item.unit_sale_price

            # Calculate proportional costs
            sale_gross_total = sum(
                si.quantity * si.unit_sale_price
                for si in sale.line_items.all()
            )

            if sale_gross_total > 0:
                proportion = item_gross / sale_gross_total
                allocated_shipping = sale.shipping_cost * proportion
                allocated_fees = sale.platform_fees * proportion
                allocated_tax = sale.tax * proportion
            else:
                allocated_shipping = allocated_fees = allocated_tax = Decimal('0.00')

            item_net = item_gross - allocated_shipping - allocated_fees - allocated_tax

            # Calculate COGS
            avg_cost = calculate_average_unit_cost(item.product, user)
            cogs = item.quantity * avg_cost if avg_cost else Decimal('0.00')

            # Calculate profit
            profit = item_net - cogs

            if set_name not in set_profits:
                set_profits[set_name] = Decimal('0.00')
            set_profits[set_name] += profit

    return [
        {'set': set_name, 'profit': float(profit)}
        for set_name, profit in sorted(set_profits.items(), key=lambda x: x[1], reverse=True)
    ]


def get_profit_by_product(user, start_date=None, end_date=None):
    """
    Calculate profit breakdown by Product.
    """
    sales = Sale.objects.filter(user=user)

    if start_date:
        sales = sales.filter(sale_date__gte=start_date)
    if end_date:
        sales = sales.filter(sale_date__lte=end_date)

    product_profits = {}

    for sale in sales:
        for item in sale.line_items.all():
            product_name = item.product.name
            product_id = str(item.product.id)

            # Calculate item revenue
            item_gross = item.quantity * item.unit_sale_price

            # Calculate proportional costs
            sale_gross_total = sum(
                si.quantity * si.unit_sale_price
                for si in sale.line_items.all()
            )

            if sale_gross_total > 0:
                proportion = item_gross / sale_gross_total
                allocated_shipping = sale.shipping_cost * proportion
                allocated_fees = sale.platform_fees * proportion
                allocated_tax = sale.tax * proportion
            else:
                allocated_shipping = allocated_fees = allocated_tax = Decimal('0.00')

            item_net = item_gross - allocated_shipping - allocated_fees - allocated_tax

            # Calculate COGS
            avg_cost = calculate_average_unit_cost(item.product, user)
            cogs = item.quantity * avg_cost if avg_cost else Decimal('0.00')

            # Calculate profit
            profit = item_net - cogs

            if product_id not in product_profits:
                product_profits[product_id] = {
                    'name': product_name,
                    'profit': Decimal('0.00')
                }
            product_profits[product_id]['profit'] += profit

    return [
        {'product': data['name'], 'profit': float(data['profit'])}
        for product_id, data in sorted(product_profits.items(), key=lambda x: x[1]['profit'], reverse=True)
    ]


def get_cashflow_over_time(user, start_date, end_date, aggregation='daily'):
    """
    Calculate cashflow (sales revenue - purchases) over time.
    Returns time series data.
    """
    # This is a simplified implementation
    # Full implementation would aggregate by day/week/month based on aggregation parameter
    purchases = Purchase.objects.filter(
        user=user,
        status='RECEIVED',
        purchase_date__gte=start_date,
        purchase_date__lte=end_date
    ).order_by('purchase_date')

    sales = Sale.objects.filter(
        user=user,
        sale_date__gte=start_date,
        sale_date__lte=end_date
    ).order_by('sale_date')

    data_points = []

    # Aggregate purchases
    for purchase in purchases:
        total_cost = sum(item.quantity * item.unit_cost for item in purchase.line_items.all())
        total_cost += purchase.delivery_fee

        data_points.append({
            'date': purchase.purchase_date.isoformat(),
            'type': 'purchase',
            'amount': -float(total_cost)
        })

    # Aggregate sales
    for sale in sales:
        gross_revenue = sum(item.quantity * item.unit_sale_price for item in sale.line_items.all())
        net_revenue = gross_revenue - sale.shipping_cost - sale.platform_fees - sale.tax

        data_points.append({
            'date': sale.sale_date.isoformat(),
            'type': 'sale',
            'amount': float(net_revenue)
        })

    return sorted(data_points, key=lambda x: x['date'])


def get_summary_metrics(user):
    """
    Get all high-level summary metrics for the dashboard.
    """
    total_invested = get_total_invested(user)
    total_profit = get_total_realized_profit(user)
    unrealized_value = get_unrealized_inventory_value(user)
    break_even = get_break_even_revenue(user)

    # Calculate overall ROI
    overall_roi = (total_profit / total_invested * 100) if total_invested > 0 else 0

    return {
        'total_invested': total_invested,
        'total_realized_profit': total_profit,
        'unrealized_inventory_value': unrealized_value,
        'overall_roi': overall_roi,
        'break_even_revenue': break_even,
        'average_profit_per_sale': get_average_profit_per_sale(user),
        'cost_breakdown': get_cost_breakdown(user),
    }
