from django.urls import path
from .views import PurchaseLivestock, TransactionHistory

urlpatterns = [
    path('purchase/', PurchaseLivestock.as_view(), name='purchase-livestock'),
    path('', TransactionHistory.as_view(), name='transaction-history'),
]