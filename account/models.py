from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from core.models import AbstractBaseModel
from asset.models import Cryptocurrency, Property, Stock, Vehicle 

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(blank=True, max_length=17, null=True, unique=True)
    is_admin = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=True)
    is_phone_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number"]

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='service_one_user_set',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='service_one_user',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='service_one_user_permissions_set', 
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='service_one_user',
    )

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_otp_expired(self):
        if self.otp_created_at is None:
            return False
        return timezone.now() > self.otp_created_at + timedelta(minutes=2)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'account_user'
        managed = False

class Player(AbstractBaseModel):
    AVATAR_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.IntegerField(unique=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coin = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    avatar = models.CharField(max_length=5, choices=AVATAR_CHOICES, default="M")
    multitap = models.IntegerField(default=1)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    last_coin_update = models.DateTimeField(default=timezone.now)

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
    
    def buy_cryptocurrency(self, cryptocurrency, quantity):
        total_cost = cryptocurrency.price * quantity
        if self.coin >= total_cost and cryptocurrency.purchasable_quantity >= quantity:
            player_crypto, created = PlayerCryptocurrency.objects.get_or_create(player=self, cryptocurrency=cryptocurrency)
            if created:
                player_crypto.quantity = quantity
            else:
                player_crypto.quantity += quantity
            cryptocurrency.purchasable_quantity -= quantity
            self.coin -= total_cost
            self.save()
            cryptocurrency.save()
            player_crypto.save()
            return True
        return False

    def sell_cryptocurrency(self, cryptocurrency, quantity):
        try:
            player_crypto = PlayerCryptocurrency.objects.get(player=self, cryptocurrency=cryptocurrency)
            if player_crypto.quantity >= quantity:
                player_crypto.quantity -= quantity
                cryptocurrency.purchasable_quantity += quantity
                self.coin += cryptocurrency.price * quantity
                self.save()
                cryptocurrency.save()
                if player_crypto.quantity == 0:
                    player_crypto.delete()
                else:
                    player_crypto.save()
                return True
        except PlayerCryptocurrency.DoesNotExist:
            return False
        return False

    def buy_property(self, property):
        if self.coin >= property.price:
            player_property, created = PlayerProperty.objects.get_or_create(player=self, property=property)
            if not created:
                return False
            self.coin -= property.price
            self.save()
            player_property.save()
            return True
        return False

    def sell_property(self, property):
        try:
            player_property = PlayerProperty.objects.get(player=self, property=property)
            self.coin += property.price
            self.save()
            player_property.delete()
            return True
        except PlayerProperty.DoesNotExist:
            return False

    def buy_stock(self, stock, quantity):
        total_cost = stock.price * quantity
        if self.coin >= total_cost and stock.purchasable_quantity >= quantity:
            player_stock, created = PlayerStock.objects.get_or_create(player=self, stock=stock)
            if created:
                player_stock.quantity = quantity
            else:
                player_stock.quantity += quantity
            stock.purchasable_quantity -= quantity
            self.coin -= total_cost
            self.save()
            stock.save()
            player_stock.save()
            return True
        return False

    def sell_stock(self, stock, quantity):
        try:
            player_stock = PlayerStock.objects.get(player=self, stock=stock)
            if player_stock.quantity >= quantity:
                player_stock.quantity -= quantity
                stock.purchasable_quantity += quantity
                self.coin += stock.price * quantity
                self.save()
                stock.save()
                if player_stock.quantity == 0:
                    player_stock.delete()
                else:
                    player_stock.save()
                return True
        except PlayerStock.DoesNotExist:
            return False
        return False

    def buy_vehicle(self, vehicle):
        if self.coin >= vehicle.price:
            player_vehicle, created = PlayerVehicle.objects.get_or_create(player=self, vehicle=vehicle)
            if not created:
                return False
            self.coin -= vehicle.price
            self.save()
            player_vehicle.save()
            return True
        return False

    def sell_vehicle(self, vehicle):
        try:
            player_vehicle = PlayerVehicle.objects.get(player=self, vehicle=vehicle)
            self.coin += vehicle.price
            self.save()
            player_vehicle.delete()
            return True
        except PlayerVehicle.DoesNotExist:
            return False
        
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
    business_image = models.ImageField(upload_to="Account/Business_images/", null=True, blank=True)

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
    

class PlayerCryptocurrency(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

class PlayerProperty(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

class PlayerStock(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2)

class PlayerVehicle(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)