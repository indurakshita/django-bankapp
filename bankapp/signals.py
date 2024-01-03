# banking/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, account_number=generate_account_number())

def generate_account_number():
    # Your logic to generate a unique account number (you might want to use UUID or another method)
    # For simplicity, a basic example is shown here.
    import random
    return f"AC-{random.randint(100000, 999999)}"
