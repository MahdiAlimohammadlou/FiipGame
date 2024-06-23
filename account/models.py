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

    def buy_business(self, business):
        if self.coin >= business.cost:
            player_business, created = PlayerBusiness.objects.get_or_create(player=self, business=business)
            if created:
                self.coin -= business.cost
                self.save()
                return True
        return False

    def upgrade_business(self, business_id):
        player_business = PlayerBusiness.objects.get(player=self, business_id=business_id)
        return player_business.upgrade()

class Business(AbstractBaseModel):
    CATEGORY_CHOICES = [
        ('shop', 'Shop'),
        ('company', 'Company'),
        ('manufacturing', 'Manufacturinfg'),
        ('import', 'Import'),
        ('mine', 'Mine'),
        ('factory', 'Factory'),
    ]

    RANKING_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ]

    name = models.CharField(max_length=100)
    base_profit = models.DecimalField(max_digits=10, decimal_places=2)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    upgrade_cost_factor = models.DecimalField(max_digits=5, decimal_places=2, default=1.15)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    ranking = models.CharField(max_length=1, choices=RANKING_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()} - {self.ranking})"

class PlayerBusiness(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def upgrade_cost(self):
        return self.business.cost * (self.business.upgrade_cost_factor ** self.level)

    def current_profit(self):
        return self.business.base_profit * self.level

    def upgrade(self):
        if self.player.coin >= self.upgrade_cost():
            self.player.coin -= self.upgrade_cost()
            self.level += 1
            self.profit = self.current_profit()
            self.save()
            self.player.save()
            return True
        return False

    def __str__(self):
        return f"{self.player.name} - {self.business.name} (Level {self.level})"