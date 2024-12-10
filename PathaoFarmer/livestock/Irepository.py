from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from farms.models import Farm

class ILivestockRepository(ABC):

    @abstractmethod
    def create_livestock_after_reg(self, farm: Farm, animal_type: str, quantity: int):
        pass
    
    
    @abstractmethod
    def get_livestock(self, farm: Farm):
        pass

    @abstractmethod
    def get_all_livestock(self, farm: Farm):
        pass

    @abstractmethod
    def list_livestock_in_marketplace(self):
        pass

    @abstractmethod
    def get_all_marketplace_livestock(self):
        pass

    @abstractmethod
    def get_marketplace_livestock_by_user(self, user: User):
        pass

    @abstractmethod
    def get_livestock_owner(self, livestock_id: int):
        pass

    @abstractmethod
    def get_livestock_by_id(self, livestock_id: int):
        pass