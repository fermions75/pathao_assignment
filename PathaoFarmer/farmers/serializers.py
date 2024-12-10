from rest_framework import serializers
from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock

class LivestockSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    class Meta:
        model = Livestock
        fields = ['type', 'price', 'market_price', 'is_listed']

class FarmSerializer(serializers.ModelSerializer):
    livestock = LivestockSerializer(many=True, read_only=True)

    class Meta:
        model = Farm
        fields = ['name', 'balance', 'livestock']

class FarmerSerializer(serializers.ModelSerializer):
    farm = FarmSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'farm']