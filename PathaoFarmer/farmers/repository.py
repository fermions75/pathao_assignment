from django.contrib.auth.models import User
from farmers.Irepository import IFarmerRepository
from farmers.serializers import FarmerSerializer

class FarmerRepository(IFarmerRepository):

    def get_farmer(self, farmer: User):
        data = FarmerSerializer(farmer)
        return data.data