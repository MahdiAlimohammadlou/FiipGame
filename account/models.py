from django.db import models
from core.models import AbstractBaseModel
from django.utils import timezone
import uuid

class Player(AbstractBaseModel):
    AVATAR_CHOICES = [
        ('M', 'Male'),  
        ('F', 'Female'),  
    ]
    name = models.CharField(max_length=100)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coin = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    avatar = models.CharField(max_length=5, choices=AVATAR_CHOICES, default="M")
    multitap = models.IntegerField(default=1)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    last_coin_update = models.DateTimeField(default=timezone.now)
    api_key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return self.name

    def buy_business(self, business):
        if self.coin >= business.cost:
            player_business, created = PlayerBusiness.objects.get_or_create(player=self, business=business)
            if created:
                self.coin -= business.cost
                player_business.profit = business.base_profit * player_business.level
                self.profit += player_business.profit
                self.save(), player_business.save()
                return True
        return False

    def upgrade_business(self, business_id):
        player_business = PlayerBusiness.objects.get(player=self, business_id=business_id)
        return player_business.upgrade()

class Business(AbstractBaseModel):
    CATEGORY_CHOICES = [
        ('مغازه', 'مغازه'),
        ('شرکت', 'شرکت'),
        ('تولیدی', 'تولیدی'),
        ('واردات', 'واردات'),
        ('معدن', 'معدن'),
        ('کارخانه', 'کارخانه'),
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

    @property
    def upgrade_cost(self):
        return self.business.cost * (self.business.upgrade_cost_factor ** self.level)
    
    @property
    def current_profit_after_upgrade(self):
        return self.business.base_profit * (self.level + 1)

    def upgrade(self):
        if self.player.coin >= self.upgrade_cost:
            self.player.coin -= self.upgrade_cost
            self.player.profit -= self.profit
            self.level += 1
            self.profit = self.level * self.business.base_profit
            self.player.profit += self.profit
            self.save()
            self.player.save()
            return True
        return False

    def __str__(self):
        return f"{self.player.name} - {self.business.name} (Level {self.level})"