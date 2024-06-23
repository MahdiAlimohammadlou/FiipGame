from django.db import models
from core.models import AbstractBaseModel
from django.utils import timezone

# Create your models here.
class Player(AbstractBaseModel):
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100, unique=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coin = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    last_coin_update = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
