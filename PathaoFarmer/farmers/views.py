from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import FarmerSerializer
from farms.repository import FarmsRepository
from livestock.repository import LivestockRepository
from PathaoFarmer.exceptions import CustomAPIException


class FarmerDetails(APIView):
    permission_classes = (IsAuthenticated,)
    farm_repository = FarmsRepository()
    livestock_repository = LivestockRepository()

    def get(self, request):
        user = User.objects.get(username=request.user)
        serializer = FarmerSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
