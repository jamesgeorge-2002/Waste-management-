from django.db import models
from django.conf import settings
from django.utils import timezone


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()  # represent bill month as first day
    paid = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        status = 'Paid' if self.paid else 'Due'
        return f"{self.user} - {self.month:%Y-%m} - {status} - ₹{self.amount}"
