from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db import transaction
from farms.models import Farm
import random
from livestock.models import Livestock
from .models import Transaction
from .serializers import PurchaseLivestockSerializer
from PathaoFarmer.exceptions import CustomAPIException
from livestock.repository import LivestockRepository
from decimal import Decimal


class PurchaseLivestock(APIView):
    permission_classes = (IsAuthenticated,)
    livestock_repository = LivestockRepository()

    def validate_purchase(self, buyer:User, seller:User, livestock:Livestock):
        if livestock.is_listed == False:
            raise CustomAPIException(detail="Livestock is not listed in the marketplace")

        if buyer == seller:
            raise CustomAPIException(detail="You cannot purchase your own livestock")

        if buyer.farm.balance < livestock.market_price:
            raise CustomAPIException(detail="Insufficient balance to purchase livestock")


    def increase_price(self, price: Decimal) -> Decimal:
        increase_percentage = Decimal(random.uniform(0.1, 0.5))  # Random percentage between 10% and 50%
        return price * (1 + increase_percentage)


    @transaction.atomic
    def post(self, request):

        serializer = PurchaseLivestockSerializer(data=request.data)
        if serializer.is_valid():
            livestock_id = serializer.validated_data['livestock_id']

            buyer = request.user
            seller = self.livestock_repository.get_livestock_owner(livestock_id)
            livestock = self.livestock_repository.get_livestock_by_id(livestock_id)

            self.validate_purchase(buyer, seller, livestock)
            print("Validation done")

            #update buyer balance
            buyer.farm.balance -= livestock.market_price
            buyer.farm.save()
            print("Buyer balance updated")
            #update seller balance
            seller.farm.balance += livestock.market_price
            seller.farm.save()
            print("Seller balance updated")
            # Create transaction
            Transaction.objects.create(buyer=buyer, seller=seller, livestock=livestock, selling_price=livestock.market_price)
            print("Transaction created")

            print(buyer.farm.balance)
            print(seller.farm.balance)
            print(buyer.farm)

            # Mark livestock as sold
            livestock.is_listed = False
            print("Livestock is listed false")
            livestock.farm = buyer.farm
            print("Livestock farm updated")
            livestock.market_price = None
            print("Livestock market price updated")
            print(livestock.price)
            print(self.increase_price(livestock.price))
            livestock.price = self.increase_price(livestock.price)
            print("Livestock price updated -- ", livestock.price)
            livestock.save()
            print("Livestock sold")
            return Response({"message": "Livestock purchased successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            