from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .calculations import (
    get_summary_metrics,
    get_profit_by_tcg,
    get_profit_by_set,
    get_profit_by_product,
    get_cashflow_over_time,
    get_cost_breakdown,
)


class SummaryMetricsView(APIView):
    """
    GET endpoint for high-level summary metrics.
    """

    def get(self, request):
        user = User.objects.first()  # Hardcoded user
        metrics = get_summary_metrics(user)
        return Response(metrics)


class ProfitByTCGView(APIView):
    """
    GET endpoint for profit breakdown by TCG.
    """

    def get(self, request):
        user = User.objects.first()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        data = get_profit_by_tcg(user, start_date, end_date)
        return Response({'data': data})


class ProfitBySetView(APIView):
    """
    GET endpoint for profit breakdown by Set.
    """

    def get(self, request):
        user = User.objects.first()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        data = get_profit_by_set(user, start_date, end_date)
        return Response({'data': data})


class ProfitByProductView(APIView):
    """
    GET endpoint for profit breakdown by Product.
    """

    def get(self, request):
        user = User.objects.first()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        data = get_profit_by_product(user, start_date, end_date)
        return Response({'data': data})


class CashflowView(APIView):
    """
    GET endpoint for cashflow time series data.
    """

    def get(self, request):
        user = User.objects.first()

        # Default to last 30 days if not specified
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)

        start_date_param = request.query_params.get('start_date')
        end_date_param = request.query_params.get('end_date')

        if start_date_param:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d').date()
        if end_date_param:
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d').date()

        aggregation = request.query_params.get('aggregation', 'daily')

        data = get_cashflow_over_time(user, start_date, end_date, aggregation)
        return Response({'data': data})


class CostBreakdownView(APIView):
    """
    GET endpoint for cost breakdown (shipping, fees, tax).
    """

    def get(self, request):
        user = User.objects.first()
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        data = get_cost_breakdown(user, start_date, end_date)
        return Response(data)
