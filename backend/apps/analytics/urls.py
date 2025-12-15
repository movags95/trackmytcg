from django.urls import path
from .views import (
    SummaryMetricsView,
    ProfitByTCGView,
    ProfitBySetView,
    ProfitByProductView,
    CashflowView,
    CostBreakdownView,
)

urlpatterns = [
    path('summary/', SummaryMetricsView.as_view(), name='analytics-summary'),
    path('profit-by-tcg/', ProfitByTCGView.as_view(), name='profit-by-tcg'),
    path('profit-by-set/', ProfitBySetView.as_view(), name='profit-by-set'),
    path('profit-by-product/', ProfitByProductView.as_view(), name='profit-by-product'),
    path('cashflow/', CashflowView.as_view(), name='cashflow'),
    path('cost-breakdown/', CostBreakdownView.as_view(), name='cost-breakdown'),
]
