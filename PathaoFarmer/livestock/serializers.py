from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Livestock


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class LivestockSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(source='farm.owner', read_only=True)
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = Livestock
        fields = '__all__'



class ListLivestockOnMarketplaceSerializer(serializers.Serializer):
    livestock_id = serializers.IntegerField(required=True)
    market_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)


    def validate_livestock_id(self, value):
        if not Livestock.objects.filter(id=value).exists():
            raise serializers.ValidationError("Livestock does not exist.")
        return value
    
    def validate_market_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Market price must be greater than 0.")
        if value >= 1000000:
            raise serializers.ValidationError("Market price must be less than 1000000.")
        return value