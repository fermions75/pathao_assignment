from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock
from livestock.Irepository import ILivestockRepository
from livestock.enums import LivestockType
from PathaoFarmer.exceptions import LivestockNotFoundException, CustomAPIException

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
    
    def list_livestock_in_marketplace(self, livestock_id: int, market_price: float, user: User):
        try:
            livestock = Livestock.objects.get(id=livestock_id, farm__owner=user)
            if livestock.is_listed:
                raise CustomAPIException(detail="Livestock is already listed in the marketplace")
            livestock.is_listed = True
            livestock.market_price = market_price
            livestock.save()
            return livestock
        except Livestock.DoesNotExist:
            raise LivestockNotFoundException()
        except Exception as e:
            raise CustomAPIException(detail=f"An error occurred: {str(e)}")
        
    def get_all_marketplace_livestock(self):
        return Livestock.objects.filter(is_listed=True)
    
    def get_marketplace_livestock_by_user(self, user: User):
        return Livestock.objects.filter(is_listed=True, farm__owner=user)
    
    def get_livestock(self, farm: Farm):
        return farm.livestock.all()