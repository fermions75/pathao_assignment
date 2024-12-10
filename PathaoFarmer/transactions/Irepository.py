from abc import ABC, abstractmethod
from django.contrib.auth.models import User
from livestock.models import Livestock

class ITransactionsRepository(ABC):

    @abstractmethod
    def create_transaction(self, buyer: User, seller:User, livestock: Livestock):
        pass
    
    @abstractmethod
    def get_all_transactions(self, user: User):
        pass