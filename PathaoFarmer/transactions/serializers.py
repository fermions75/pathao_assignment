from rest_framework import serializers
from django.contrib.auth.models import User
from livestock.models import Livestock
from livestock.repository import LivestockRepository

class PurchaseLivestockSerializer(serializers.Serializer):
    livestock_id = serializers.IntegerField(required=True)
