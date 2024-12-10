from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock
from livestock.Irepository import ILivestockRepository
from livestock.enums import LivestockType
from PathaoFarmer.exceptions import LivestockNotFoundException, CustomAPIException
import random
from decimal import Decimal


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
    
    def list_livestock_in_marketplace(self, livestock_id: int, market_price: float, owner: User):
        try:
            livestock = Livestock.objects.get(id=livestock_id, farm__owner=owner)
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
    
    def get_livestock(self, farm: Farm):
        return farm.livestock.all()
    
    def get_livestock_by_id(self, livestock_id: int):
        value = Livestock.objects.filter(id=livestock_id)
        if not value.exists():
            raise LivestockNotFoundException()
        return value[0]
    
    def get_livestock_owner(self, livestock_id: int):
        value = Livestock.objects.filter(id=livestock_id)
        if not value.exists():
            raise LivestockNotFoundException()
        return value[0].farm.owner
    
    def increase_price(self, price: Decimal) -> Decimal:
        increase_percentage = Decimal(random.uniform(0.1, 0.5))  # Random percentage between 10% and 50%
        return price * (1 + increase_percentage)
    
    def mark_livestock_as_sold(self, livestock: Livestock, owner: User):
        try:
            livestock.is_listed = False
            livestock.farm = owner.farm
            livestock.price = self.increase_price(livestock.market_price)
            livestock.market_price = None
            livestock.save()
            return livestock
        except Livestock.DoesNotExist:
            raise LivestockNotFoundException()
        except Exception as e:
            raise CustomAPIException(detail=f"An error occurred: {str(e)}")