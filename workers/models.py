from django.db import models
from django.conf import settings
from locations.models import LocalBody, Ward


class WorkerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    worker_id = models.CharField(max_length=50, unique=True)
    local_body = models.ForeignKey(LocalBody, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_wards = models.ManyToManyField(Ward, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    id_proof = models.ImageField(upload_to='worker_id_proofs/', null=True, blank=True)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.worker_id})"
