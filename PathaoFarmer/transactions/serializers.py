from rest_framework import serializers
from django.contrib.auth.models import User
from livestock.models import Livestock
from livestock.repository import LivestockRepository
from .models import Transaction

class PurchaseLivestockSerializer(serializers.Serializer):
    livestock_id = serializers.IntegerField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class LivestockSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Livestock
        fields = ['type', 'price', 'market_price', 'is_listed']


class TransactionSerializer(serializers.ModelSerializer):
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    livestock = LivestockSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'livestock', 'buyer', 'seller', 'selling_price', 'sell_date']