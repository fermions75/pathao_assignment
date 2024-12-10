from django.contrib.auth.models import User
from farms.models import Farm
from farms.Irepository import IFarmsRepository


class FarmsRepository(IFarmsRepository):

    def create_farm(self, farmer: User):
        farm = Farm.objects.create(owner=farmer)
        return farm

    def get_farm(self, farmer: User):
        return Farm.objects.get(owner=farmer)

    def update_farm_balance(self, farmer: User, amount: float):
        farm = Farm.objects.get(owner=farmer)
        farm.balance = amount
        farm.save()
        return farm.balance



