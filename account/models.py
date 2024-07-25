from django.db import models
from core.models import AbstractBaseModel
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from datetime import timedelta

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