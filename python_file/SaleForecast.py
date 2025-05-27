import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX

orders = pd.read_csv('sample_data/online_order_aligned.csv')
orders['OrderDate'] = pd.to_datetime(orders['OrderDate'])
orders.set_index('OrderDate', inplace=True)
monthly_sales = orders.resample('M')['TotalAmount'].sum()

# Train/test split
train = monthly_sales[:-3]
test = monthly_sales[-3:]

# Fit SARIMA model
model = SARIMAX(train, order=(1,1,1), seasonal_order=(1,1,1,12))
results = model.fit()

# Forecast
forecast = results.forecast(steps=3)
print("Forecasted sales:", forecast)