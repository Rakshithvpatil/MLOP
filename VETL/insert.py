import os
import sys
import django
import time
import random
from datetime import datetime, timedelta

# Setup Django environment FIRST
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VETL.settings')
django.setup()

# NOW import models after Django setup
from Product.models import Product
from Product.views import exporttoCSV

CATEGORIES = ['Electronics', 'Books', 'Grocery', 'Toys', 'Clothing']
VENDORS = ['Vendor A', 'Vendor B', 'Vendor C', 'Vendor D', 'Vendor E']

# PRODUCT_NAMES = {
#     'Electronics': ['Laptop', 'Phone', 'Tablet', 'Speaker', 'Headphones', 'Camera', 'Monitor'],
#     'Books': ['Python Guide', 'Web Design', 'Data Science', 'AI Handbook', 'Django Tutorial'],
#     'Grocery': ['Organic Milk', 'Fresh Bread', 'Green Tea', 'Olive Oil', 'Pasta', 'Rice'],
#     'Toys': ['Action Figure', 'Board Game', 'Puzzle', 'Doll', 'Car Model', 'Building Blocks'],
#     'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Sneakers', 'Hat', 'Sweater', 'Dress']
# }


# print("done reading")
def create_random_product():
    # category = random.choice(CATEGORIES)
    # product_names = PRODUCT_NAMES[category]
    # base_name = random.choice(product_names)
    now = datetime.now()

    # # Create unique product name
    # timestamp = int(time.time())
    # product_name = f"{base_name}_{timestamp}"
    # now = datetime.now()
    product = Product.objects.create(
        product_name=f"Product_{int(time.time())}", # UNique name using timestamp
        product_category=random.choice(CATEGORIES),
        # product_vendor=random.choice(VENDORS),
        product_manufacturing_date=now,
        product_expiry_date=now+timedelta(days=random.randint(30,365))
    )
    print(f"Inserted: {product.product_name} at {now}")
    # return product

if __name__ == '__main__':
    print("Product insertion every 5 seconds.Press Ctrl + C to stop")
    try:
        while True:
            create_random_product()
            # response = exporttoCSV()
            # data = json.loads(response.content.decode('utf-8'))
            time.sleep(5)
    except KeyboardInterrupt:
        print("Stopped by user.")