from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from farms.models import Farm

class ILivestockRepository(ABC):

    @abstractmethod
    def create_livestock_after_reg(self, farm: Farm, animal_type: str, quantity: int):
        pass

    @abstractmethod
    def get_all_livestock(self, farm: Farm):
        pass

    @abstractmethod
    def list_livestock_in_marketplace(self):
        pass