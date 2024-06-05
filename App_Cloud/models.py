from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# USER
class MyUser(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)  
    address = models.CharField(max_length=1000,default="None")
    photo = models.ImageField(null=False,blank=False,upload_to="user")
    phone = models.CharField(max_length=1000,default="None")
    trusted = models.BooleanField(default=False)

# Category
class RestaurantCategories(models.Model):
    category = models.CharField(max_length=400,default="Nothing")
    def __str__(self) -> str:
        return self.category
    
# Restaurant    
class Restaurant(models.Model):
    name = models.CharField(max_length=1000,default="None")
    location = models.CharField(max_length=100,default="None")
    category = models.ForeignKey(RestaurantCategories, on_delete=models.CASCADE,default=1)
    min_price = models.IntegerField(default=0)
    max_price = models.IntegerField(default=0)
    seats = models.IntegerField(default=0)
    tables = models.IntegerField(default=0)
    photo = models.ImageField(null=False,blank=False,upload_to="restaurant")
    def __str__(self) -> str:
        return self.name

class FoodItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=1)
    title = models.CharField(max_length=1000,default="None")
    price = models.IntegerField(default=0)
    photo = models.ImageField(null=False,blank=False,upload_to="food")
    def __str__(self) -> str:
        return self.title

class Table(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=1)
    seats = models.IntegerField(default=0)
    booking_status = models.BooleanField(default=False)
    

class BookingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=1)
    table = models.ForeignKey(Table, on_delete=models.CASCADE,default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

class FoodOrder(models.Model):
    item = models.ForeignKey(FoodItem, on_delete=models.CASCADE,default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    bill = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    order_status = models.BooleanField(default=False)

