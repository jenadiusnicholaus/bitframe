from django.contrib import admin

# Register your models here.
from products.models import Frame, Categories, Product


admin.site.register(Categories)
admin.site.register(Product)