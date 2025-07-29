from django.contrib import admin
from .models import Product,Customers,Order,Author,Book,Actor,Movie
# Register your models here.

admin.site.register(Product)
admin.site.register(Customers)
admin.site.register(Order)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Actor)
admin.site.register(Movie)