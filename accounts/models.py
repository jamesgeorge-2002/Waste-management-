from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('house', 'House'),
        ('shop', 'Shop'),
        ('company', 'Company'),
        ('industry', 'Industry'),
    ]

    LOCAL_BODY_TYPE_CHOICES = [
        ('panchayat', 'Panchayat'),
        ('municipality', 'Municipality'),
    ]

    full_name = models.CharField(max_length=255, blank=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=True)
    local_body_type = models.CharField(max_length=20, choices=LOCAL_BODY_TYPE_CHOICES, blank=True)
    local_body = models.ForeignKey('locations.LocalBody', null=True, blank=True, on_delete=models.SET_NULL)
    ward = models.ForeignKey('locations.Ward', null=True, blank=True, on_delete=models.SET_NULL)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    is_worker = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() or self.username
