from django.db import models
from django.conf import settings


class Reward(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    reason = models.CharField(max_length=255, blank=True)
    awarded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.points} pts"


class Penalty(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    reason = models.CharField(max_length=255, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - Penalty ₹{self.amount}"