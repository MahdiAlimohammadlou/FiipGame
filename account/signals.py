import string
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Player

def generate_referral_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@receiver(post_save, sender=Player)
def create_referral_code(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        instance.referral_code = generate_referral_code()
        instance.save()