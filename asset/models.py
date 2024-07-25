from django.db import models
from core.models import AbstractBaseModel

# Create your models here.
class Cryptocurrency(AbstractBaseModel):
    name = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    purchasable_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    currency_logo = models.ImageField(upload_to="Asset/currency_logo_images", null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Property(AbstractBaseModel):
    name = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    property_img = models.ImageField(upload_to="Asset/property_images", null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Stock(AbstractBaseModel):
    name = models.CharField(max_length=225)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    purchasable_quantity = models.DecimalField(max_digits=12, decimal_places=2)
    stock_logo = models.ImageField(upload_to="Asset/stock_logo_images", null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
class Vehicle(AbstractBaseModel):

    VEHICLE_TYPES = [
        ("ماشین", "ماشین"),
        ("هواپیما", "هواپیما"),
        ("کشتی", "کشتی"),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    vehicle_img = models.ImageField(upload_to="Asset/vehicle_images", null=True, blank=True)
    vehicle_type = models.CharField(max_length=255, choices=VEHICLE_TYPES)
