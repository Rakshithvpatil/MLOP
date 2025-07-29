import os
import django
import pandas as pd
from django.conf import settings
from django.db import connection

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VETL.settings')
django.setup()

from Product.models import Product, Customers, Order

def export_mysql_to_csv():
    csv_dir = os.path.join(settings.BASE_DIR,'csv_exports')
    os.makedirs(csv_dir,exist_ok=True)

    #Export Products
    products = Product.objects.all().values()
    products_df = pd.DataFrame(products)
    products_df.to_csv(os.path.join(csv_dir,'product.csv'),index=False)

    #Export Customers
    customers = Customers.objects.all().values()
    customers_df = pd.DataFrame(customers)
    customers_df.to_csv(os.path.join(csv_dir,'customers.csv'),index=False)

    #Export Orders
    orders = Order.objects.all().values()
    orders_df = pd.DataFrame(orders)
    orders_df.to_csv(os.path.join(csv_dir,'orders.csv'),index=False)

    # Export Combined Analytics Data
    combined_query = """
    SELECT 
        p.product_name, p.product_category, p.product_vendor,
        p.product_manufacturing_date, o.quantity, o.order_time,
        c.cust_name
    FROM Product_product p
    LEFT JOIN Product_order o ON p.id = o.product_id
    LEFT JOIN Product_customers c ON o.customer_id = c.id   
    """ 
    combined_df = pd.read_sql_query(combined_query, connection)
    combined_df.to_csv(os.path.join(csv_dir, 'analytics_data.csv'), index=False)

    return csv_dir