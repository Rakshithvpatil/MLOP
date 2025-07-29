#conversion of pyton native into Custom data objects is serialization
# conversion of complex data into easy data is called serialization
from rest_framework import serializers
from .models import Product,Customers,User,Profile,Author,Book,Actor,Movie,Order

class ProductSerializer(serializers.ModelSerializer):
        class Meta:
                model = Product
                fields = '__all__'  # searlize all fields of the Products model
        
class CustomerSerializer(serializers.ModelSerializer):
        class Meta:
                model = Customers
                fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
         model = Order
         fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields='__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields='__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Author
        fields='__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model=Book
        fields='__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
       model=Actor
       fields='__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model=Movie
        fields='__all__'

