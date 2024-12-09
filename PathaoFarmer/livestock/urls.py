from django.urls import path
from .views import ListLivestockOnMarketplace

urlpatterns = [
    path('marketplace/', ListLivestockOnMarketplace.as_view(), name='list-livestock'),
]