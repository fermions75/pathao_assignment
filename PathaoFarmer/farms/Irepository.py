from abc import ABC, abstractmethod
from django.contrib.auth.models import User


class IFarmsRepository(ABC):
    @abstractmethod
    def create_farm(self, farmer: User):
        pass

    @abstractmethod
    def get_farm(self, farmer: User):
        pass

    @abstractmethod
    def update_farm_balance(self, farmer: User, amount: float):
        pass