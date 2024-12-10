from abc import ABC, abstractmethod
from django.contrib.auth.models import User

class IFarmsRepository(ABC):
    @abstractmethod
    def create_farm(self, user: User):
        pass

    @abstractmethod
    def get_farm(self, user: User):
        pass

    # @abstractmethod
    # def get_farm_balance(self, user: User):
    #     pass

    # @abstractmethod
    # def update_farm_balance(self, user: User, amount: float):
    #     pass

    # @abstractmethod
    # def delete_farm(self, user: User):
    #     pass

    # @abstractmethod
    # def get_all_farms(self):
    #     pass

    # @abstractmethod
    # def get_farm_owner(self, farm_id: int):
    #     pass