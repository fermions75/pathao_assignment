from django.contrib.auth.models import User
from farms.models import Farm
from livestock.models import Livestock
from transactions.models import Transaction
from transactions.Irepository import ITransactionsRepository
from livestock.enums import LivestockType
from PathaoFarmer.exceptions import LivestockNotFoundException, CustomAPIException
from django.db.models import Q

class TransactionsRepository(ITransactionsRepository):

    def create_transaction(self, buyer: User, seller:User, livestock: Livestock):
        Transaction.objects.create(buyer=buyer, seller=seller, livestock=livestock, selling_price=livestock.market_price)

    def get_all_transactions(self, user: User):
        val = Transaction.objects.filter(Q(buyer=user) | Q(seller=user))
        return val