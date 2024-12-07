from django.db import models
from SsideApp.models import Product

# Create your models here.
class UserRegistration(models.Model):
    id=models.AutoField
    fullname = models.CharField(max_length=150)
    email=models.EmailField(max_length=254,unique=True)
    password = models.CharField(max_length=150)
    isactive = models.BooleanField(default=True)
    usertype = models.IntegerField(default=0)
    profilephoto=models.ImageField(upload_to="user/",default="user/1.png")
    date_joined =models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    locality = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)

class Cart(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(null=True,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.quantity * self.product.itemprice
    
class Order(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    ordered_date = models.DateTimeField(auto_now_add=True)

