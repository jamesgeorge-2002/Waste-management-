from django.db import models


LOCAL_BODY_TYPE_CHOICES = [
    ('panchayat', 'Panchayat'),
    ('municipality', 'Municipality'),
]


class LocalBody(models.Model):
    name = models.CharField(max_length=255)
    body_type = models.CharField(max_length=20, choices=LOCAL_BODY_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_body_type_display()})"


class Ward(models.Model):
    local_body = models.ForeignKey(LocalBody, related_name='wards', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField()

    class Meta:
        unique_together = ('local_body', 'number')

    def __str__(self):
        return f"Ward {self.number} - {self.name}"
