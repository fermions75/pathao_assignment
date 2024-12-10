from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from livestock.repository import LivestockRepository
from django.contrib.auth.models import User
from .serializers import LivestockSerializer, ListLivestockOnMarketplaceSerializer
from PathaoFarmer.exceptions import CustomAPIException


class ListLivestockOnMarketplace(APIView):
    """
    This endpoint will allow the authenticated user to list their livestock in the marketplace
    """
    permission_classes = (IsAuthenticated,)
    livestock_repository = LivestockRepository()

    def post(self, request):
        serializer = ListLivestockOnMarketplaceSerializer(data=request.data)

        if serializer.is_valid():
            livestock_id = serializer.validated_data['livestock_id']
            market_price = serializer.validated_data['market_price']
            user = User.objects.get(username=request.user)
            livestock = self.livestock_repository.list_livestock_in_marketplace(livestock_id, market_price, user)
            serializer = LivestockSerializer(livestock)
            return Response(serializer.data, status=status.HTTP_200_OK)
        raise CustomAPIException(detail=serializer.errors, code=status.HTTP_400_BAD_REQUEST)
    

    def get(self, request):
        livestock = self.livestock_repository.get_all_marketplace_livestock()
        serializer = LivestockSerializer(livestock, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

