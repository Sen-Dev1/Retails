import pandas as pd
from sklearn.ensemble import RandomForestClassifier

orders = pd.read_csv('sample_data/online_order_aligned.csv')
fraud = pd.read_csv('sample_data/fraud_alert.csv')

orders['IsFraud'] = orders['OnlineOrderID'].isin(fraud['OrderID']).astype(int)
X = orders[['TotalAmount']]  # Add more features as needed
y = orders['IsFraud']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier()
clf.fit(X_train, y_train)
print("Fraud prediction accuracy:", clf.score(X_test, y_test))