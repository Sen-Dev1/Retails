import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

orders = pd.read_csv('sample_data/online_order_aligned.csv')
fraud = pd.read_csv('sample_data/fraud_alert.csv')

print("Order columns:", orders.columns)  # Debug: See available columns

orders['IsFraud'] = orders['OnlineOrderID'].isin(fraud['OrderID']).astype(int)

# Example: Try using a different column if TotalAmount doesn't exist
# X = orders[['TotalAmount']]  # Replace with actual column name
# y = orders['IsFraud']

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# clf = RandomForestClassifier()
# clf.fit(X_train, y_train)
# print("Fraud prediction accuracy:", clf.score(X_test, y_test))