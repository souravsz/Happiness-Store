from django.contrib import admin
from . models import products,Cart,CartItem,Payment

admin.site.register(products)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
    