from django.db import models
from django.conf import settings
from locations.models import Ward
from workers.models import WorkerProfile


WASTE_TYPE_CHOICES = [
    ('wet', 'Wet'),
    ('dry', 'Dry'),
    ('ewaste', 'E-waste'),
    ('hazardous', 'Hazardous'),
]

PICKUP_STATUS = [
    ('requested', 'Requested'),
    ('assigned', 'Assigned'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('missed', 'Missed'),
]


class WasteRecord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='waste_records')
    waste_type = models.CharField(max_length=20, choices=WASTE_TYPE_CHOICES)
    entered_weight = models.FloatField()
    verified_weight = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='waste_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.waste_type} - {self.entered_weight}kg"


class Pickup(models.Model):
    waste_record = models.OneToOneField(WasteRecord, on_delete=models.CASCADE, related_name='pickup')
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, blank=True)
    scheduled_date = models.DateField(null=True, blank=True)
    assigned_worker = models.ForeignKey(WorkerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=PICKUP_STATUS, default='requested')
    worker_proof_image = models.ImageField(upload_to='pickup_proofs/', null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Pickup {self.id} - {self.waste_record.user} - {self.status}"
