from django.db import models
from farms.models import Farm
from livestock.enums import LivestockType

class Livestock(models.Model):
    type = models.CharField(max_length=10, choices=[(tag, tag.value) for tag in LivestockType])
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Base price
    market_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_listed = models.BooleanField(default=False)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="livestock")

    def __str__(self):
        return f"{self.type.capitalize()} (Farm: {self.farm.name})"
