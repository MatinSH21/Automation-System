from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Employee, Profile


@receiver(post_save, sender=Employee)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(employee=instance)


@receiver(post_save, sender=Employee)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
