from django.contrib import admin
from django.urls import path, include
from farmers.views import FarmerDetails

urlpatterns = [
    path('', FarmerDetails.as_view(), name='farmer-details'),
]