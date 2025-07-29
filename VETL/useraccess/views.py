from django.shortcuts import render
from rest_framework.views  import APIView
from .serializers import RegisterSerializer,UserSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics,status



class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer

    def create(self,request,*args,**kwargs):
        response=super().create(request,*args,**kwargs)
        user=User.objects.get(username=response.data['username'])
        #refresh=RefreshToken.for_user(user)
        return Response({
            'message':'User registered Succesful',
            'user':{
               'username':user.username,
                'email':user.email
            }
        })

class LoginView(APIView):
    def post(self,request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username,password=password)

        if user is not None:
            refresh=RefreshToken.for_user(user)
            return Response({
            'message':'User Logged in',
            'user':{
               'username':user.username,
                'email':user.email
            },
            'token' : {
                'refresh':str(refresh),
                'access':str(refresh.access_token)
            }})
        
        return Response({'error': 'Invalid Cred'},status=status.HTTP_400_BAD_REQUEST)

# Create your views here.
