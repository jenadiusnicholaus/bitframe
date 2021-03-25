from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.contrib.auth.models import Group
from django.utils import timezone
from django_rest_passwordreset.signals import reset_password_token_created
from rest_framework.reverse import reverse

from enterapi.settings import AUTH_USER_MODEL
from django.db.models.signals import post_save
from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
import uuid


class TimestampedModel(models.Model):
    # A timestamp representing when this object was created.
    created_at = models.DateTimeField(default=timezone.now, null=True)

    # A timestamp reprensenting when this object was last updated.
    updated_at = models.DateTimeField(default=timezone.now, null=True)

    class Meta:
        abstract = True

        ordering = ['-created_at', '-updated_at']


class UserManager(BaseUserManager):
    """
        Django requires that custom users define their own Manager class. By
        inheriting from `BaseUserManager`, we get a lot of the same code used by
        Django to create a `User` for free.
        All we have to do is override the `create_user` function which we will use
        to create `User` objects.
        """

    def create_user(self, email, username=None, password=None, **extra_fields):
        """Create and return a `User` with an email and password."""

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.username = username
        user.save(using=self._db)

        return user

    @property
    def is_active(self):
        return True

    def create_superuser(self, email=None, username=None, password=None, **extra_fields):

        if not email:
            raise TypeError("superuser must have an email address")
        if not password:
            raise TypeError('User must have password')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.username = username
        user.is_superuser = True
        user.admin = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        """
        Returns a string representation of this `User`.
        This string is used when a `User` is printed in the console.
        """
        return str(self.email)


class UserProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    age = models.PositiveIntegerField(null=True, blank=False)
    image_url = models.ImageField(upload_to='user_profile_pic', null=True)

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"

    def __str__(self):
        return str(self.user.email)

    @property
    def get_imag_url(self):
        try:
            if self.image_url and hasattr(self.image_url, 'url'):
                return self.image_url.url
        except:
            return None


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created=False, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


# @receiver(post_save,sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, db_constraint=False)
    location = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Address'

    def __str__(self):
        return self.user.email
