from django.urls import path
from .views import PurchaseLivestock, TransactionHistory

urlpatterns = [
    path('all', TransactionHistory.as_view(), name='transaction-history'),
    path('purchase/', PurchaseLivestock.as_view(), name='purchase-livestock'),
]