from django.urls import path
from .views import PurchaseLivestock

urlpatterns = [
    path('purchase/', PurchaseLivestock.as_view(), name='purchase-livestock'),
]