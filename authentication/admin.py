from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.

from authentication.models import User,UserProfile

admin.site.register(User)
admin.site.register(UserProfile)
admin.site.unregister(Group)
