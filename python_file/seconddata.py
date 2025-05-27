import pandas as pd
import numpy as np
import os
from faker import Faker

fake = Faker()
np.random.seed(42)

DATA_DIR = "sample_data"
os.makedirs(DATA_DIR, exist_ok=True)

# Load already generated core tables
customers = pd.read_csv(f"{DATA_DIR}/customer.csv")
products = pd.read_csv(f"{DATA_DIR}/product.csv")
stores = pd.read_csv(f"{DATA_DIR}/store.csv")
channels = pd.read_csv(f"{DATA_DIR}/advertising_channel.csv")
online_orders = pd.read_csv(f"{DATA_DIR}/online_order_aligned.csv")
order_lines = pd.read_csv(f"{DATA_DIR}/order_lines.csv")
promotions = pd.read_csv(f"{DATA_DIR}/promotion.csv")

# Helper functions for random selection
def rand_choice(series, n):
    return np.random.choice(series, n)

# Table generation logic
table_generators = {
    "financial_transactions.csv": lambda: pd.DataFrame({
        "TransactionID": [f"FT{str(i).zfill(7)}" for i in range(1, 4001)],
        "CustomerID": rand_choice(customers["CustomerID"], 4000),
        "StoreID": rand_choice(stores["StoreID"], 4000),
        "Amount": np.random.uniform(-500, 2000, 4000).round(2),
        "TransactionDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(4000)],
        "Type": np.random.choice(['Sale', 'Refund', 'GiftCard'], 4000)
    }),
    "restock_order.csv": lambda: pd.DataFrame({
        "RestockOrderID": [f"RO{str(i).zfill(6)}" for i in range(1, 1001)],
        "StoreID": rand_choice(stores["StoreID"], 1000),
        "SupplierID": [f"SUP{str(i).zfill(4)}" for i in np.random.randint(1, 61, 1000)],
        "OrderDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)],
        "Status": np.random.choice(['Ordered', 'Received', 'Cancelled'], 1000)
    }),
    "gift_card.csv": lambda: pd.DataFrame({
        "GiftCardID": [f"GC{str(i).zfill(6)}" for i in range(1, 1001)],
        "CustomerID": rand_choice(customers["CustomerID"], 1000),
        "Amount": np.random.uniform(10, 500, 1000).round(2),
        "IssueDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)],
        "Active": np.random.choice([0, 1], 1000)
    }),
    "gift_card_transaction.csv": lambda: pd.DataFrame({
        "GiftCardTransactionID": [f"GCTX{str(i).zfill(6)}" for i in range(1, 2001)],
        "GiftCardID": rand_choice([f"GC{str(i).zfill(6)}" for i in range(1, 1001)], 2000),
        "StoreID": rand_choice(stores["StoreID"], 2000),
        "Amount": np.random.uniform(-100, 100, 2000).round(2),
        "TransactionDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(2000)]
    }),
    "inventory_costing.csv": lambda: pd.DataFrame({
        "CostingID": [f"IC{str(i).zfill(6)}" for i in range(1, 1001)],
        "StoreID": rand_choice(stores["StoreID"], 1000),
        "ProductID": rand_choice(products["ProductID"], 1000),
        "EffectiveDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)],
        "Cost": np.random.uniform(1, 400, 1000).round(2)
    }),
    "inventory_movement.csv": lambda: pd.DataFrame({
        "MovementID": [f"IM{str(i).zfill(6)}" for i in range(1, 2001)],
        "StoreID": rand_choice(stores["StoreID"], 2000),
        "ProductID": rand_choice(products["ProductID"], 2000),
        "Quantity": np.random.randint(-20, 50, 2000),
        "MovementDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(2000)]
    }),
    "cart_abandonment.csv": lambda: pd.DataFrame({
        "CartID": [f"CART{str(i).zfill(6)}" for i in range(1, 1001)],
        "CustomerID": rand_choice(customers["CustomerID"], 1000),
        "RecoveryAttempted": np.random.choice([0, 1], 1000),
        "AbandonDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)]
    }),
    "abandoned_cart.csv": lambda: pd.DataFrame({
        "AbandonedCartID": [f"AC{str(i).zfill(6)}" for i in range(1, 1001)],
        "CartID": rand_choice([f"CART{str(i).zfill(6)}" for i in range(1, 1001)], 1000),
        "RecoveryEmailSent": np.random.choice([0, 1], 1000)
    }),
    "coupon.csv": lambda: pd.DataFrame({
        "CouponID": [f"COUP{str(i).zfill(5)}" for i in range(1, 201)],
        "DiscountPercentage": np.random.randint(5, 50, 200),
        "ValidFrom": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(200)],
        "ValidTo": [fake.date_between(start_date='-1y', end_date='today') for _ in range(200)]
    }),
    "coupon_redemption.csv": lambda: pd.DataFrame({
        "RedemptionID": [f"CR{str(i).zfill(6)}" for i in range(1, 1001)],
        "CouponID": rand_choice([f"COUP{str(i).zfill(5)}" for i in range(1, 201)], 1000),
        "CustomerID": rand_choice(customers["CustomerID"], 1000),
        "RedemptionDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(1000)]
    }),
    # Add similar lambdas for all other missing tables...
}

# Generate and save all remaining tables
for fname, generator in table_generators.items():
    print(f"Generating {fname} ...")
    df = generator()
    df.to_csv(f"{DATA_DIR}/{fname}", index=False)

print("All remaining sample tables generated in the 'sample_data' directory.")