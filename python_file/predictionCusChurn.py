import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# 1. Load data
customers = pd.read_csv('sample_data/customer.csv')
orders = pd.read_csv('sample_data/online_order_aligned.csv')
loyalty = pd.read_csv('sample_data/customer_loyalty.csv')

# 2. Feature engineering (example: total orders, loyalty program)
order_counts = orders.groupby('CustomerID').size().reset_index(name='OrderCount')
customers = customers.merge(order_counts, on='CustomerID', how='left').fillna(0)
customers['IsLoyalty'] = customers['CustomerID'].isin(loyalty['CustomerID']).astype(int)

# 3. Define churn (example: no orders in last 6 months)
orders['OrderDate'] = pd.to_datetime(orders['OrderDate'])
recent_orders = orders[orders['OrderDate'] > pd.Timestamp.now() - pd.Timedelta(days=180)]
customers['Churned'] = ~customers['CustomerID'].isin(recent_orders['CustomerID'])

# 4. Prepare data
X = customers[['OrderCount', 'IsLoyalty']]
y = customers['Churned'].astype(int)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Train model
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# 6. Evaluate
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))