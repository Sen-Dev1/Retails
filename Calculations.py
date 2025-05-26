# Example in Python (using pandas)
import pandas as pd

# Load data
customers = pd.read_csv('customer.csv')
orders = pd.read_csv('order_lines.csv')

# Calculate order value
orders['OrderValue'] = orders['Quantity'] * orders['UnitPrice']

# Total spend per customer
customer_spend = orders.groupby('CustomerID')['OrderValue'].sum().reset_index()
customer_spend.columns = ['CustomerID', 'TotalSpend']