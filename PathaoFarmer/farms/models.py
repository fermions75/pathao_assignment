from django.db import models
from django.contrib.auth.models import User

class Farm(models.Model):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=500000.00)
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="farm")

    def save(self, *args, **kwargs):
        if not self.name:  # Set name only if it's not already set
            self.name = f"{self.owner.email.split('@')[0]}'s Farm"
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.name} owned by {self.owner.username}"