from django.contrib import admin
from . models import products,Cart,CartItem

admin.site.register(products)
admin.site.register(Cart)
admin.site.register(CartItem)
    