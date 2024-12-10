from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock

class ILivestockRepository(ABC):

    @abstractmethod
    def create_livestock_after_reg(self, farm: Farm, animal_type: str, quantity: int):
        pass

    @abstractmethod
    def list_livestock_in_marketplace(self, livestock_id: int, market_price: float, owner: User):
        pass

    @abstractmethod
    def get_all_marketplace_livestock(self):
        pass

    @abstractmethod
    def get_livestock_owner(self, livestock_id: int):
        pass

    @abstractmethod
    def get_livestock_by_id(self, livestock_id: int):
        pass

    @abstractmethod
    def mark_livestock_as_sold(self, livestock: Livestock, owner: User):
        pass