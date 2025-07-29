import pandas as pd
import os
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

def get_product_analytics():
    csv_dir = os.path.join(settings.BASE_DIR, 'csv_exports')
    
    from .export_mysql_data import export_mysql_to_csv
    export_mysql_to_csv()
    
    # Read products CSV (has data)
    products_df = pd.read_csv(os.path.join(csv_dir, 'product.csv'))
    
    # Handle empty CSV files
    customers_file = os.path.join(csv_dir, 'customers.csv')
    if os.path.getsize(customers_file) > 10:
        customers_df = pd.read_csv(customers_file)
    else:
        customers_df = pd.DataFrame()
    
    orders_file = os.path.join(csv_dir, 'orders.csv')
    if os.path.getsize(orders_file) > 10:
        orders_df = pd.read_csv(orders_file)
    else:
        orders_df = pd.DataFrame()
    
    analytics_file = os.path.join(csv_dir, 'analytics_data.csv')
    if os.path.getsize(analytics_file) > 10:
        analytics_df = pd.read_csv(analytics_file)
    else:
        analytics_df = pd.DataFrame()
    
    total_products = len(products_df)
    total_customers = len(customers_df)
    total_orders = len(orders_df)
    
    # Category distribution (only from products)
    category_distribution = {}
    if not products_df.empty and 'product_category' in products_df.columns:
        clean_categories = products_df.dropna(subset=['product_category'])
        clean_categories = clean_categories[clean_categories['product_category'].str.strip() != '']
        category_distribution = clean_categories['product_category'].value_counts().to_dict()
    
    # Vendor distribution (only from products)
    vendor_distribution = {}
    if not products_df.empty and 'product_vendor' in products_df.columns:
        clean_vendors = products_df.dropna(subset=['product_vendor'])
        clean_vendors = clean_vendors[clean_vendors['product_vendor'].str.strip() != '']
        vendor_distribution = clean_vendors['product_vendor'].value_counts().to_dict()
    
    # Recent products
    recent_products_count = 0
    if not products_df.empty:
        products_df['product_manufacturing_date'] = pd.to_datetime(products_df['product_manufacturing_date'], format='mixed')
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_products_count = len(products_df[products_df['product_manufacturing_date'] >= seven_days_ago])
    
    return {
        'total_products': total_products,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'active_customers': 0,
        'recent_products_7_days': recent_products_count,
        'category_distribution': category_distribution,
        'vendor_distribution': vendor_distribution,
        'top_selling_products': [],
        'analytics_timestamp': timezone.now().isoformat()
    }

def get_sales_trend_data():
    return []