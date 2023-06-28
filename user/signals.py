from django.dispatch import receiver
from .models import Profile
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save

@receiver(post_save, sender=get_user_model())
def create_profile(sender, created, instance, **kwargs):
    if created == True:
        Profile.objects.create(staff = instance)

@receiver(post_save, sender=get_user_model())
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.profile.save()