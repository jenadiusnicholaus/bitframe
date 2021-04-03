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
    ('monthly', 'Monthly'),
    ('3-month', '3-Month'),
    ('6-month', '6-Month'),
    ('yearly', 'Yearly'),
)


class FrameCategories(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)

    class Meta:
        verbose_name_plural = 'Frames categories'

    def __str__(self):
        return self.title


class Frame(models.Model):

    categories = models.ForeignKey(FrameCategories, on_delete=models.SET_NULL, null=True,related_name='frameCategories')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='frame_images', null=True)
    name = models.CharField(unique=True, max_length=20, null=True, )
    description = models.TextField(null=True)
    location = models.CharField(max_length=200, null=True)
    capacity = models.IntegerField(default=0)
    frame_type = models.CharField(max_length=20, choices=FRAME_TYPE)
    price = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    updated_at = models.DateTimeField(default=timezone.now, null=True)
    duration = models.CharField(max_length=20, choices=RENT_DURATION, null=True)

    class Meta:
        verbose_name_plural = 'Frames'

    def __str__(self):
        return self.name

    @property
    def count_products(self):
        return self.product_set.count()
