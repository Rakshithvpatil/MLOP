import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Button
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
  Line
} from 'recharts';
import { Refresh as RefreshIcon } from '@mui/icons-material';

const Dashboard = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [productsData, setProductsData] = useState([]);
  const [customersData, setCustomersData] = useState([]);
  const [ordersData, setOrdersData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Colors for charts
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

  useEffect(() => {
    fetchAllData();
    // Refresh data every 30 seconds
    const interval = setInterval(fetchAllData, 30000);
    return () => clearInterval(interval);
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      
      // Fetch analytics data
      const analyticsResponse = await fetch('http://localhost:8000/api/analytics/');
      let analyticsResult = null;
      
      if (analyticsResponse.ok) {
        analyticsResult = await analyticsResponse.json();
        setAnalyticsData(analyticsResult);
      }

      // Fetch products data
      try {
        const productsResponse = await fetch('http://localhost:8000/api/products/');
        if (productsResponse.ok) {
          const productsResult = await productsResponse.json();
          setProductsData(productsResult);
        }
      } catch (err) {
        console.log('Products endpoint not available');
      }

      // Fetch customers data
      try {
        const customersResponse = await fetch('http://localhost:8000/api/customers/');
        if (customersResponse.ok) {
          const customersResult = await customersResponse.json();
          setCustomersData(customersResult);
        }
      } catch (err) {
        console.log('Customers endpoint not available');
      }

      // Fetch orders data
      try {
        const ordersResponse = await fetch('http://localhost:8000/api/orders/');
        if (ordersResponse.ok) {
          const ordersResult = await ordersResponse.json();
          setOrdersData(ordersResult);
        }
      } catch (err) {
        console.log('Orders endpoint not available');
      }

      setLoading(false);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          Loading Dashboard...
        </Typography>
      </Box>
    );
  }

  // Prepare data for charts
  const categoryData = analyticsData?.category_distribution 
    ? Object.entries(analyticsData.category_distribution).map(
        ([category, count]) => ({ category, count })
      )
    : [];

  const vendorData = analyticsData?.vendor_distribution 
    ? Object.entries(analyticsData.vendor_distribution).map(
        ([vendor, count]) => ({ vendor, count })
      )
    : [];

  const topProductsData = analyticsData?.top_selling_products?.map(product => ({
    name: product.product__product_name,
    orders: product.order_count
  })) || [];

  // Basic statistics from fetched data
  const totalProducts = productsData.length || analyticsData?.total_products || 0;
  const totalCustomers = customersData.length || analyticsData?.total_customers || 0;
  const totalOrders = ordersData.length || analyticsData?.total_orders || 0;

  return (
    <Box p={3}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4" gutterBottom>
          VETL Analytics Dashboard
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchAllData}
          disabled={loading}
        >
          Refresh Data
        </Button>
      </Box>
      
      {error && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          Some data may not be available. Backend server: {error}
        </Alert>
      )}
      
      {/* Summary Cards */}
      <Grid container spacing={3} mb={4}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                Total Products
              </Typography>
              <Typography variant="h4">
                {totalProducts}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Real-time count
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                Total Orders
              </Typography>
              <Typography variant="h4">
                {totalOrders}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                All orders
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                Total Customers
              </Typography>
              <Typography variant="h4">
                {totalCustomers}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                Registered customers
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                Active Customers
              </Typography>
              <Typography variant="h4">
                {analyticsData?.active_customers || '0'}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                With orders
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3}>
        {/* Category Distribution */}
        {categoryData.length > 0 ? (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Products by Category
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={categoryData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="category" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="count" fill="#8884d8" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        ) : (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Products by Category
                </Typography>
                <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                  <Typography color="textSecondary">
                    No category data available
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Vendor Distribution */}
        {vendorData.length > 0 ? (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Vendor Distribution
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <PieChart>
                    <Pie
                      data={vendorData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ vendor, count }) => `${vendor}: ${count}`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="count"
                    >
                      {vendorData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        ) : (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Vendor Distribution
                </Typography>
                <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                  <Typography color="textSecondary">
                    No vendor data available
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Recent Products Table/Chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activity
              </Typography>
              {productsData.length > 0 ? (
                <Box>
                  <Typography variant="body2" color="textSecondary">
                    Last 5 products added:
                  </Typography>
                  <Box mt={2}>
                    {productsData.slice(-5).map((product, index) => (
                      <Box key={index} p={1} border={1} borderColor="grey.300" borderRadius={1} mb={1}>
                        <Typography variant="body1">
                          <strong>{product.product_name}</strong> - {product.product_category}
                        </Typography>
                        <Typography variant="caption" color="textSecondary">
                          Vendor: {product.product_vendor}
                        </Typography>
                      </Box>
                    ))}
                  </Box>
                </Box>
              ) : (
                <Typography color="textSecondary">
                  No product data available. Start by adding some products!
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Last Updated */}
      <Box mt={3}>
        <Typography variant="caption" color="textSecondary">
          Last updated: {new Date().toLocaleString()}
          {analyticsData?.analytics_timestamp && (
            ` | Server data: ${new Date(analyticsData.analytics_timestamp).toLocaleString()}`
          )}
        </Typography>
      </Box>
    </Box>
  );
};

export default Dashboard;