import uuid

from django.conf import settings
from django.db import models

# Create your models here.
from django.utils import timezone

FRAME_TYPE = (
    ('wholeSeller', 'Whole seller'),
    ('retailer', 'Retailer'),
)

RENT_DURATION = (
    ('month', 'Monthly'),
    ('year', 'Yearly'),
)


class Frame(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(unique=True, max_length=20, null=True, )
    capacity = models.IntegerField(default=0)
    frame_type = models.CharField(max_length=20, choices=FRAME_TYPE)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    updated_at = models.DateTimeField(default=timezone.now, null=True)
    duration = models.CharField(max_length=20, choices=RENT_DURATION, null=True)

    def __str__(self):
        return self.name
