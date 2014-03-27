from django.db import models
from django.db.models.signals import post_save
from accounts.models import User


class Profile(models.Model):
    full_name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=64, unique=True)
    camps = models.CharField(max_length=100, blank=True, null=True,)
    art = models.CharField(max_length=100, blank=True, null=True,)
    phone = models.CharField(max_length=16)    
    user = models.OneToOneField(User, related_name='profile')

def create_volunteer_profile(sender, instance, created, **kwargs):
    #Create a user profile when a new user account is created
    if created == True:
        Profile.objects.get_or_create(user=instance)

post_save.connect(create_volunteer_profile, sender=User)