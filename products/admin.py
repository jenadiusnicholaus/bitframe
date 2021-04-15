from django.contrib import admin



from products.models import Frame, Categories, Product, OrderedProducts, Orders

admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(OrderedProducts)
admin.site.register(Orders)

