from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from rest_framework import viewsets,generics,status
from .models import Product, Customers, User, Profile, Author, Book, Actor, Movie, Order
from .serializers import ProductSerializer,CustomerSerializer,UserSerializer,ProfileSerializer, AuthorSerializer, BookSerializer, ActorSerializer, MovieSerializer, OrderSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import AllowAny

import csv
import pandas as pd
import os
from django.conf import settings
from .analytics import get_product_analytics, get_sales_trend_data
from .export_mysql_data import export_mysql_to_csv

class ProductViewSet(viewsets.ModelViewSet):
       queryset = Product.objects.all()
       serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
      queryset = Customers.objects.all()
      serializer_class = CustomerSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class ProductAPIView(APIView):
    def get(self, request, *args, **kwargs):
        product_item = Product.objects.all()
        serializer=ProductSerializer(product_item,many=True)
        return Response(serializer.data)

    def post(self,request,*args,**kwargs):
         serializer=ProductSerializer(data=request.data)
         if serializer.is_valid():
             serializer.save() #post to store the data
             return Response(serializer.data,status=status.HTTP_201_CREATED)

class CustomerAPIView(APIView):
    def get(self, request):
        customers = Customers.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class OrderAPIView(APIView):
    def get(self, request, pk=None):
        if pk:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# NEW: Simple Analytics API Views
class AnalyticsAPIView(APIView):
    def get(self, request):
        analytics_data = get_product_analytics()
        return Response(analytics_data)

class ExportCSVAPIView(APIView):
    def get(self, request):
        csv_dir = export_mysql_to_csv()
        return Response({
            'status': 'success',
            'message': 'CSV export completed',
            'csv_directory': csv_dir
        })

class RefreshAnalyticsAPIView(APIView):
    def post(self, request):
        export_mysql_to_csv()
        analytics_data = get_product_analytics()
        return Response({
            'status': 'success',
            'data': analytics_data
        })

def exporttoCSV():
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_exports')
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, 'exported_products.csv')
    
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Category', 'Vendor', 'Mfg Date', 'Exp Date'])
        
        for product in Product.objects.all():
            writer.writerow([
                product.product_name,
                product.product_category,
                product.product_vendor,
                product.product_manufacturing_date,
                product.product_expiry_date
            ])
    
    df = pd.read_csv(csv_path)
    books_records = df[df['Category'] == "Books"]["Name"] if 'Category' in df.columns else []
    
    return JsonResponse({
        "message": "CSV exported successfully",
        "total_products": len(df),
        "books_count": len(books_records),
        "books": books_records.tolist()
    })