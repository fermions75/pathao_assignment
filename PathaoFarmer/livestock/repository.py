from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock
from livestock.Irepository import ILivestockRepository
from livestock.enums import LivestockType

class LivestockRepository(ILivestockRepository):

    def create_livestock_after_reg(self, farm: Farm):
        Livestock.objects.bulk_create(
            [
                Livestock(farm=farm, type=LivestockType.COW.value, price=10000.00) for _ in range(5)
            ]    + 
            [
                Livestock(farm=farm, type=LivestockType.GOAT.value, price=8000.00) for _ in range(5)
            ] + 
            [
                Livestock(farm=farm, type=LivestockType.SHEEP.value, price=5000.00) for _ in range(3)
            ]
        )
        

    def get_all_livestock(self, farm: Farm):
        return farm.livestock.all()