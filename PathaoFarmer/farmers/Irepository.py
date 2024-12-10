from abc import ABC, abstractmethod
from django.contrib.auth.models import User

class IFarmerRepository(ABC):
    @abstractmethod
    def get_farmer(self, farmer: User):
        pass