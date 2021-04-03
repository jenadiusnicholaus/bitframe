import uuid

from django.conf import settings
from django.db import models
from django.utils import timezone

from authentication.models import TimestampedModel
from frame.models import Frame


class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=12, null=True)
    image = models.ImageField(upload_to='product_category_images', null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        verbose_name_plural = 'Product categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product_categories = models.ForeignKey(Categories, on_delete=models.SET_NULL, null  = True)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE, null=True ,related_name='frame')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=12, null=True)
    image = models.ImageField(upload_to='product_images', null=True)
    price = models.IntegerField()
    description = models.TextField( null=True)
    created_at = models.DateTimeField(default=timezone.now, null=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        verbose_name_plural = 'Products '

    def __str__(self):
        return self.name

    def get_image_url(self):
        try:
            if self.image and hasattr(self.image, 'url'):
                return self.image.url
        except:
            return None
