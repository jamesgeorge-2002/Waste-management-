from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WasteRecord, Pickup
from locations.models import Ward


@receiver(post_save, sender=WasteRecord)
def create_pickup_for_waste(sender, instance, created, **kwargs):
    if created:
        ward = None
        if instance.user.ward:
            ward = instance.user.ward
        Pickup.objects.create(waste_record=instance, ward=ward)
