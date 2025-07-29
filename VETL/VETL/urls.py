"""
URL configuration for VETL project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
# from Product.views import ProductViewSet,CustomerViewSet
from Product.views import ProductViewSet, CustomerViewSet, UserViewSet, ProfileViewSet,AuthorViewSet, BookViewSet, ActorViewSet, MovieViewSet, OrderViewSet,ProductAPIView, CustomerAPIView, OrderAPIView, ExportCSVAPIView, AnalyticsAPIView, RefreshAnalyticsAPIView
from useraccess.views import RegisterView,LoginView
# product_list = ProductViewSet.as_view ({
#     'get': 'list',
#     'post':'create'
# })
# customers_list = CustomerViewSet.as_view ({
#     'get': 'list',
#     'post':'create'
# })

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'movies', MovieViewSet)
router.register(r'products-viewset', ProductViewSet)
router.register(r'customers-viewset', CustomerViewSet)
router.register(r'orders-viewset', OrderViewSet)

urlpatterns = [

    path('admin/', admin.site.urls),
    
    # Include router URLs for ViewSets
    path('api/', include(router.urls)),

    path("user/",UserViewSet.as_view({'get':'list','post':'create'})),
    path("profile/",ProfileViewSet.as_view({'get':'list','post':'create'})),
    path("author/",AuthorViewSet.as_view({'get':'list','post':'create'})),
    path("book/",BookViewSet.as_view({'get':'list','post':'create'})),
    path("actor/",ActorViewSet.as_view({'get':'list','post':'create'})),
    path("user/",MovieViewSet.as_view({'get':'list','post':'create'})),
    path("api/orders/",OrderAPIView.as_view(),name='order-create'),
    path("api/orders/<int:pk>",OrderAPIView.as_view(),name='order-detail'),
    path("api/customers/",CustomerAPIView.as_view(),name='Customer-detail'),
    path("api/products/",ProductAPIView.as_view(),name='product-list'),
    path('api/export-csv/', ExportCSVAPIView.as_view(), name='export-csv'),
    path('api/analytics/refresh/', RefreshAnalyticsAPIView.as_view(), name='refresh-analytics'),
    path('api/analytics/', AnalyticsAPIView.as_view(), name='analytics'),
    path('api/register/',RegisterView.as_view(),name='register'),
    path('api/login/', LoginView.as_view(),name='login')
]




