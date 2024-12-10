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
from .serializers import PurchaseLivestockSerializer, TransactionSerializer
from PathaoFarmer.exceptions import CustomAPIException
from livestock.repository import LivestockRepository
from transactions.repository import TransactionsRepository
from farms.repository import FarmsRepository
from decimal import Decimal


class PurchaseLivestock(APIView):
    """
    This endpoint will allow the authenticated user to purchase livestock from the marketplace
    """
    permission_classes = (IsAuthenticated,)
    livestock_repository = LivestockRepository()
    transaction_repository = TransactionsRepository()
    farm_repository = FarmsRepository()

    def validate_purchase(self, buyer:User, seller:User, livestock:Livestock):
        if livestock.is_listed == False:
            raise CustomAPIException(detail="Livestock is not listed in the marketplace")

        if buyer == seller:
            raise CustomAPIException(detail="You cannot purchase your own livestock")

        if buyer.farm.balance < livestock.market_price:
            raise CustomAPIException(detail="Insufficient balance to purchase livestock")

    @transaction.atomic
    def post(self, request):
        serializer = PurchaseLivestockSerializer(data=request.data)
        if serializer.is_valid():
            livestock_id = serializer.validated_data['livestock_id']

            buyer = request.user
            seller = self.livestock_repository.get_livestock_owner(livestock_id)
            livestock = self.livestock_repository.get_livestock_by_id(livestock_id)

            self.validate_purchase(buyer, seller, livestock)

            #update buyer balance
            self.farm_repository.update_farm_balance(buyer, buyer.farm.balance - livestock.market_price)

            #update seller balance
            self.farm_repository.update_farm_balance(seller, seller.farm.balance + livestock.market_price)

            # Create transaction
            self.transaction_repository.create_transaction(buyer, seller, livestock)

            # Mark livestock as sold
            self.livestock_repository.mark_livestock_as_sold(livestock, buyer)

            return Response({"message": "Livestock purchased successfully"}, status=status.HTTP_200_OK)

        raise CustomAPIException(detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    

class TransactionHistory(APIView):
    """
    This endpoint will return the transaction history of the authenticated user
    """
    permission_classes = (IsAuthenticated,)
    transaction_repository = TransactionsRepository()

    def get(self, request):
        transactions = self.transaction_repository.get_all_transactions(request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            