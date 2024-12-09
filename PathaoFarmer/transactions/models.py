from django.db import models
from django.contrib.auth.models import User
from livestock.models import Livestock

class Transaction(models.Model):
    livestock = models.ForeignKey(Livestock, on_delete=models.CASCADE, related_name="transactions")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.livestock.type} sold by {self.seller.username} to {self.buyer.username}"
