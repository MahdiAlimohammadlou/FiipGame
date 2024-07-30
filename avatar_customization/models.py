from django.db import models
from core.models import AbstractBaseModel

# Create your models here.
class Item(AbstractBaseModel):

    CATEGORY_CHOICES = [
        ('fitness', 'Fitness Situation'),
        ('wear', 'Wear'),
        ('accessory', 'Accessory'),
    ]

    name = models.CharField(max_length=100)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()})"
