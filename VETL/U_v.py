import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VETL.settings')
django.setup()

from Product.models import Product

VENDORS = ['Vendor A', 'Vendor B', 'Vendor C', 'Vendor D', 'Vendor E']

products_to_update = Product.objects.filter(product_vendor__isnull=True) | Product.objects.filter(product_vendor='')

for product in products_to_update:
    product.product_vendor = random.choice(VENDORS)
    product.save()

print(f"Updated {products_to_update.count()} products")