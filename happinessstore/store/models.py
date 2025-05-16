from django.db import models
from django.contrib.auth.models import User

class products(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='product_images/')
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
class CartItem(models.Model):
    cart= models.ForeignKey(Cart,related_name="items",on_delete=models.CASCADE)
    product = models.ForeignKey(products,on_delete=models.CASCADE)
    quantity =models.SmallIntegerField(default=1)
    @property
    def subtotal(self):
        return self.quantity * self.product.price
    
    