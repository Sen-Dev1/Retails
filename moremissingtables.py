import os
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

DATA_DIR = "sample_data"

required_tables = [
    # ... (your full list here, as before)
]

existing_tables = set(f for f in os.listdir(DATA_DIR) if f.endswith('.csv'))
missing_tables = [t for t in required_tables if t not in existing_tables]

def load_csv(name):
    path = os.path.join(DATA_DIR, name)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

customers = load_csv("customer.csv")
products = load_csv("product.csv")
stores = load_csv("store.csv")
orders = load_csv("online_order_aligned.csv")
employees = load_csv("employee.csv")
channels = load_csv("advertising_channel.csv")
promotions = load_csv("promotion.csv")
suppliers = load_csv("supplier.csv") if os.path.exists(os.path.join(DATA_DIR, "supplier.csv")) else None

def rand_choice(series, n):
    return np.random.choice(series, n) if series is not None else ["" for _ in range(n)]

table_generators = {
    "restock_request.csv": lambda: pd.DataFrame({
        "RestockRequestID": [f"RR{str(i).zfill(6)}" for i in range(1, 501)],
        "StoreID": rand_choice(stores["StoreID"], 500),
        "ProductID": rand_choice(products["ProductID"], 500),
        "RequestDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Quantity": np.random.randint(1, 100, 500)
    }),
    "price_history.csv": lambda: pd.DataFrame({
        "PriceHistoryID": [f"PH{str(i).zfill(6)}" for i in range(1, 1001)],
        "ProductID": rand_choice(products["ProductID"], 1000),
        "StoreID": rand_choice(stores["StoreID"], 1000),
        "Date": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)],
        "Price": np.random.uniform(5, 500, 1000).round(2)
    }),
    "carrier.csv": lambda: pd.DataFrame({
        "CarrierID": [f"CAR{str(i).zfill(4)}" for i in range(1, 21)],
        "CarrierName": [fake.company() for _ in range(20)]
    }),
    "marketing_campaign.csv": lambda: pd.DataFrame({
        "CampaignID": [f"MC{str(i).zfill(5)}" for i in range(1, 101)],
        "ChannelID": rand_choice(channels["ChannelID"], 100),
        "StartDate": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(100)],
        "EndDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)],
        "Budget": np.random.uniform(1000, 10000, 100).round(2)
    }),
    "store_closure.csv": lambda: pd.DataFrame({
        "ClosureID": [f"SC{str(i).zfill(5)}" for i in range(1, 21)],
        "StoreID": rand_choice(stores["StoreID"], 20),
        "ClosureDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(20)],
        "Reason": [fake.sentence() for _ in range(20)]
    }),
    "online_order_line.csv": lambda: pd.DataFrame({
        "OrderLineID": [f"OOL{str(i).zfill(7)}" for i in range(1, 2001)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 2000),
        "ProductID": rand_choice(products["ProductID"], 2000),
        "Quantity": np.random.randint(1, 5, 2000),
        "UnitPrice": rand_choice(products["UnitPrice"], 2000)
    }),
    "customer_feedback.csv": lambda: pd.DataFrame({
        "FeedbackID": [f"CF{str(i).zfill(6)}" for i in range(1, 1001)],
        "CustomerID": rand_choice(customers["CustomerID"], 1000),
        "FeedbackText": [fake.sentence() for _ in range(1000)],
        "Date": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)]
    }),
    "delivery_tracking.csv": lambda: pd.DataFrame({
        "TrackingID": [f"DT{str(i).zfill(7)}" for i in range(1, 1001)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 1000),
        "Status": np.random.choice(['Shipped', 'In Transit', 'Delivered'], 1000),
        "UpdateDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)]
    }),
    # Add more generators for each missing table, always referencing existing sample_data tables for foreign keys
}

def safe_to_csv(df, fname):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        df.to_csv(path, index=False)
        print(f"Generated {fname}")

for t in missing_tables:
    if t in table_generators:
        safe_to_csv(table_generators[t](), t)
    else:
        print(f"No generator defined for {t}. Please add one to table_generators.")

print("Done. All missing tables (with defined generators) have been generated with referential integrity.")