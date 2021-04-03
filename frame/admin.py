from django.contrib import admin

# Register your models here.
from frame.models import Frame, FrameCategories

admin.site.register(Frame)
admin.site.register(FrameCategories)