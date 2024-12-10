from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializers import FarmerSerializer
from farmers.repository import FarmerRepository
from PathaoFarmer.exceptions import CustomAPIException


class FarmerDetails(APIView):
    permission_classes = (IsAuthenticated,)
    farms_repository = FarmerRepository()


    def get(self, request):
        user = User.objects.get(username=request.user)
        farmer_data = self.farms_repository.get_farmer(user)
        return Response(farmer_data, status=status.HTTP_200_OK)
