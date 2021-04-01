from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Account

# creates profile for user
@receiver(post_save, sender=Account)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# saves profile for user
@receiver(post_save, sender=Account)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
