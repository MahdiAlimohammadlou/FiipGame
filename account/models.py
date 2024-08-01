from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
from core.models import AbstractBaseModel
from asset.models import Business, Cryptocurrency, Property, Stock, Vehicle 
from avatar_customization.models import Item
from core.exceptions import NotEnoughMoney, InvalidQuantity

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

class Avatar(AbstractBaseModel):
    AVATAR_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=AVATAR_CHOICES)
    avatar_image = models.ImageField(upload_to="Account/avatar_images/", null=True, blank=True)

    def __str__(self) -> str:
        return self.name

class Player(AbstractBaseModel):
    user = models.IntegerField(unique=True)
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coin = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    avatar = models.ForeignKey(Avatar, on_delete=models.CASCADE)
    multitap = models.IntegerField(default=1)
    referral_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    last_coin_update = models.DateTimeField(default=timezone.now)

    @property
    def is_anonymous(self):
        return False

    def __str__(self):
        return f"id:{self.id},user:{self.user}"

    def buy_business(self, business):
        if self.coin < business.cost:
            raise NotEnoughMoney("Not enough coins to buy the business.")
        player_business, created = PlayerBusiness.objects.get_or_create(player=self, business=business)
        if created:
            self.coin -= business.cost
            player_business.profit = business.base_profit * player_business.level
            self.profit += player_business.profit
            self.save()
            player_business.save()
            return True
        return False

    def upgrade_business(self, business_id):
        player_business = PlayerBusiness.objects.get(player=self, business_id=business_id)
        if not player_business.upgrade():
            raise NotEnoughMoney("Not enough coins to upgrade the business.")
        return True
    
    def buy_cryptocurrency(self, cryptocurrency, quantity):
        total_cost = cryptocurrency.price * quantity
        if self.coin < total_cost:
            raise NotEnoughMoney("Not enough coins to buy the cryptocurrency.")
        if cryptocurrency.purchasable_quantity < quantity:
            raise InvalidQuantity("Not enough cryptocurrency available to purchase.")
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

    def sell_cryptocurrency(self, cryptocurrency, quantity):
        try:
            player_crypto = PlayerCryptocurrency.objects.get(player=self, cryptocurrency=cryptocurrency)
            if player_crypto.quantity < quantity:
                raise InvalidQuantity("Not enough cryptocurrency to sell.")
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
            raise InvalidQuantity("No cryptocurrency found to sell.")
    
    def buy_property(self, property):
        if self.coin < property.price:
            raise NotEnoughMoney("Not enough coins to buy the property.")
        player_property, created = PlayerProperty.objects.get_or_create(player=self, property=property)
        if not created:
            raise InvalidQuantity("Property already owned.")
        self.coin -= property.price
        self.save()
        player_property.save()
        return True

    def sell_property(self, property):
        try:
            player_property = PlayerProperty.objects.get(player=self, property=property)
            self.coin += property.price
            self.save()
            player_property.delete()
            return True
        except PlayerProperty.DoesNotExist:
            raise InvalidQuantity("No property found to sell.")

    def buy_stock(self, stock, quantity):
        total_cost = stock.price * quantity
        if self.coin < total_cost:
            raise NotEnoughMoney("Not enough coins to buy the stock.")
        if stock.purchasable_quantity < quantity:
            raise InvalidQuantity("Not enough stock available to purchase.")
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

    def sell_stock(self, stock, quantity):
        try:
            player_stock = PlayerStock.objects.get(player=self, stock=stock)
            if player_stock.quantity < quantity:
                raise InvalidQuantity("Not enough stock to sell.")
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
            raise InvalidQuantity("No stock found to sell.")

    def buy_vehicle(self, vehicle):
        if self.coin < vehicle.price:
            raise NotEnoughMoney("Not enough coins to buy the vehicle.")
        player_vehicle, created = PlayerVehicle.objects.get_or_create(player=self, vehicle=vehicle)
        if not created:
            raise InvalidQuantity("Vehicle already owned.")
        self.coin -= vehicle.price
        self.save()
        player_vehicle.save()
        return True

    def sell_vehicle(self, vehicle):
        try:
            player_vehicle = PlayerVehicle.objects.get(player=self, vehicle=vehicle)
            self.coin += vehicle.price
            self.save()
            player_vehicle.delete()
            return True
        except PlayerVehicle.DoesNotExist:
            raise InvalidQuantity("No vehicle found to sell.")

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
    quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True)

class PlayerProperty(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)

class PlayerStock(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, null=True)

class PlayerVehicle(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

class PlayerItem(AbstractBaseModel):
    player = models.ForeignKey('Player', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.player} - {self.item} - {'Active' if self.is_active else 'Inactive'}"