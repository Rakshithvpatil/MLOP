from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=90)
    product_category = models.CharField(max_length=90)
    product_vendor = models.CharField(max_length=90)
    product_manufacturing_date=models.DateTimeField()
    product_expiry_date = models.DateTimeField(null=True,blank=True)

class Customers(models.Model):
    cust_name = models.CharField(max_length=90)
    cust_email = models.CharField(max_length=90)
    cust_address = models.CharField(max_length=90)
    cust_phone=models.CharField(max_length=12)  

class Order(models.Model):
    customer = models.ForeignKey(Customers,on_delete=models.CASCADE,null=True, blank=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,null=True, blank=True)
    order_time=models.DateTimeField()
    quantity = models.IntegerField(default=1)

class User(models.Model):
    user_name=models.CharField(max_length=30)
    user_email=models.CharField(max_length=30)


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    description=models.CharField(max_length=30)    

class Author(models.Model):
    auth_name=models.CharField(max_length=30)

class Book(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,related_name='books')

class Actor(models.Model):
    act_name=models.CharField(max_length=30)

class Movie(models.Model):
    title = models.CharField(max_length=30)
    actors = models.ManyToManyField(Actor, related_name='movies')
    movie_name = models.ManyToManyField(Actor,related_name='actor')