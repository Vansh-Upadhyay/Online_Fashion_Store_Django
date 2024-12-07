from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    category_image = models.ImageField(upload_to='category', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
class Product(models.Model):
    id=models.AutoField
    itemName=models.CharField(max_length=150)
    itemDescription=models.CharField(max_length=150)
    itemprice=models.FloatField()
    item_image=models.ImageField(upload_to="products/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)