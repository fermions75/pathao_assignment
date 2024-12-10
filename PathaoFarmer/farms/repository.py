from django.contrib.auth.models import User
from farms.models import Farm
from farms.Irepository import IFarmsRepository


class FarmsRepository(IFarmsRepository):

    def create_farm(self, user: User):
        farm = Farm.objects.create(owner=user)
        return farm

    # def get_all_farms(self):
    #     return Farm.objects.all()

    def get_farm(self, user: User):
        return Farm.objects.get(owner=user)

    # def get_farm_balance(self, user: User):
    #     farm = Farm.objects.get(owner=user)
    #     return farm.balance

    # def update_farm_balance(self, user: User, amount: float):
    #     farm = Farm.objects.get(owner=user)
    #     farm.balance += amount
    #     farm.save()
    #     return farm.balance

    # def delete_farm(self, user: User):
    #     farm = Farm.objects.get(owner=user)
    #     farm.delete()

    # def get_farm_owner(self, farm_id: int):
    #     farm = Farm.objects.get(id=farm_id)
    #     return farm.owner

    # def create_animal(self, farm: Farm, animal_type: str, quantity: int):
    #     animal = Animal.objects.create(farm=farm, type=animal_type, quantity=quantity)
    #     return animal

    # def get_all_animals(self, farm: Farm):
    #     return farm.animals.all()

    # def get_animal(self, farm: Farm, animal_type: str):
    #     return farm.animals.get(type=animal_type)

    # def update_animal_quantity(self, farm: Farm, animal_type: str, quantity: int):
    #     animal = farm.animals.get(type=animal_type)
    #     animal.quantity += quantity
    #     animal.save()
    #     return animal.quantity

    # def delete_animal(self, farm: Farm, animal_type: str):
    #     animal = farm.animals.get(type=animal_type)
    #     animal.delete()