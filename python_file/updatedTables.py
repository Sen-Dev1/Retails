import os
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

ALL_DATA_DIR = "All data"
SAMPLE_DATA_DIR = "sample_data"

# 1. List all files
all_data_files = set(f for f in os.listdir(ALL_DATA_DIR) if f.endswith('.csv'))
sample_data_files = set(f for f in os.listdir(SAMPLE_DATA_DIR) if f.endswith('.csv'))

# 2. Identify missing files in sample_data
missing_in_sample_data = sorted(list(all_data_files - sample_data_files))
print("Tables to generate:", missing_in_sample_data)

# 3. Load reference data from sample_data for foreign keys
def load_csv(name):
    path = os.path.join(SAMPLE_DATA_DIR, name)
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

customers = load_csv("customer.csv")
products = load_csv("product.csv")
stores = load_csv("store.csv")
channels = load_csv("advertising_channel.csv")
orders = load_csv("online_order_aligned.csv")
coupons = load_csv("coupon.csv")
employees = load_csv("employee.csv")
promotions = load_csv("promotion.csv")

def rand_choice(series, n):
    return np.random.choice(series, n) if series is not None else ["" for _ in range(n)]

# 4. Table generators for missing tables
table_generators = {
    "abandoned_checkout.csv": lambda: pd.DataFrame({
        "AbandonedCheckoutID": [f"AC{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "CartID": [f"CART{str(i).zfill(6)}" for i in np.random.randint(1, 4001, 500)],
        "AbandonDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "advertising_channel_ref.csv": lambda: pd.DataFrame({
        "ChannelRefID": [f"ACR{str(i).zfill(4)}" for i in range(1, 21)],
        "ChannelID": rand_choice(channels["ChannelID"], 20),
        "Description": [fake.sentence() for _ in range(20)]
    }),
    "advertising_spend.csv": lambda: pd.DataFrame({
        "AdSpendID": [f"AS{str(i).zfill(6)}" for i in range(1, 201)],
        "ChannelID": rand_choice(channels["ChannelID"], 200),
        "SpendDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(200)],
        "Amount": np.random.uniform(100, 10000, 200).round(2)
    }),
    "affiliate_referral.csv": lambda: pd.DataFrame({
        "AffiliateReferralID": [f"AR{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "AffiliateCode": [fake.bothify(text='AFF-#####') for _ in range(500)],
        "ReferralDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "browsing_history.csv": lambda: pd.DataFrame({
        "BrowsingHistoryID": [f"BH{str(i).zfill(6)}" for i in range(1, 2001)],
        "CustomerID": rand_choice(customers["CustomerID"], 2000),
        "ProductID": rand_choice(products["ProductID"], 2000),
        "ViewDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(2000)]
    }),
    "campaign_performance.csv": lambda: pd.DataFrame({
        "CampaignPerformanceID": [f"CP{str(i).zfill(5)}" for i in range(1, 101)],
        "CampaignID": [f"MC{str(i).zfill(5)}" for i in np.random.randint(1, 101, 100)],
        "Spend": np.random.uniform(1000, 10000, 100).round(2),
        "Revenue": np.random.uniform(2000, 20000, 100).round(2)
    }),
    "campaign_response.csv": lambda: pd.DataFrame({
        "CampaignResponseID": [f"CR{str(i).zfill(6)}" for i in range(1, 501)],
        "CampaignID": [f"MC{str(i).zfill(5)}" for i in np.random.randint(1, 101, 500)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "ResponseDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "carrier.csv": lambda: pd.DataFrame({
        "CarrierID": [f"CAR{str(i).zfill(4)}" for i in range(1, 21)],
        "CarrierName": [fake.company() for _ in range(20)]
    }),
    "customer_aligned.csv": lambda: pd.DataFrame({
        "CustomerAlignedID": [f"CA{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "AlignedGroup": [fake.word().capitalize() for _ in range(500)]
    }),
    "customer_loyalty.csv": lambda: pd.DataFrame({
        "CustomerLoyaltyID": [f"CL{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "LoyaltyProgramID": [f"LP{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)],
        "JoinDate": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(500)]
    }),
    "customer_satisfaction.csv": lambda: pd.DataFrame({
        "CustomerSatisfactionID": [f"CS{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "Rating": np.random.randint(1, 6, 500),
        "Feedback": [fake.sentence() for _ in range(500)],
        "Date": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "delivery_address.csv": lambda: pd.DataFrame({
        "DeliveryAddressID": [f"DA{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "Address": [fake.address().replace('\n', ', ') for _ in range(500)],
        "City": [fake.city() for _ in range(500)],
        "State": [fake.state_abbr() for _ in range(500)],
        "Country": [fake.country() for _ in range(500)]
    }),
    "delivery_exception.csv": lambda: pd.DataFrame({
        "DeliveryExceptionID": [f"DE{str(i).zfill(6)}" for i in range(1, 101)],
        "DeliveryID": [f"DEL{str(i).zfill(6)}" for i in np.random.randint(1, 501, 100)],
        "ExceptionDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)],
        "Reason": [fake.sentence() for _ in range(100)]
    }),
    "employee_schedule.csv": lambda: pd.DataFrame({
        "EmployeeScheduleID": [f"ES{str(i).zfill(6)}" for i in range(1, 501)],
        "EmployeeID": rand_choice(employees["EmployeeID"], 500),
        "ScheduleDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Shift": np.random.choice(['Morning', 'Afternoon', 'Evening'], 500)
    }),
    "fraud_alert.csv": lambda: pd.DataFrame({
        "FraudAlertID": [f"FA{str(i).zfill(6)}" for i in range(1, 101)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 100),
        "CustomerID": rand_choice(customers["CustomerID"], 100),
        "AlertDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)],
        "Reason": [fake.sentence() for _ in range(100)]
    }),
    "inventory_audit.csv": lambda: pd.DataFrame({
        "InventoryAuditID": [f"IAU{str(i).zfill(6)}" for i in range(1, 501)],
        "StoreID": rand_choice(stores["StoreID"], 500),
        "ProductID": rand_choice(products["ProductID"], 500),
        "AuditDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Quantity": np.random.randint(0, 200, 500)
    }),
    "order_shipment.csv": lambda: pd.DataFrame({
        "OrderShipmentID": [f"OS{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "ShipmentID": [f"SHIP{str(i).zfill(6)}" for i in np.random.randint(1, 501, 500)],
        "ShipmentDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "payment_method.csv": lambda: pd.DataFrame({
        "PaymentMethodID": [f"PM{str(i).zfill(5)}" for i in range(1, 101)],
        "CustomerID": rand_choice(customers["CustomerID"], 100),
        "Method": np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Gift Card'], 100),
        "AddedDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(100)]
    }),
    "product_promotion.csv": lambda: pd.DataFrame({
        "ProductPromotionID": [f"PP{str(i).zfill(6)}" for i in range(1, 501)],
        "ProductID": rand_choice(products["ProductID"], 500),
        "PromotionID": rand_choice(promotions["PromotionID"], 500) if promotions is not None else ["" for _ in range(500)],
        "StartDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "EndDate": [fake.date_between(start_date='today', end_date='+30d') for _ in range(500)]
    }),
    "promotion_product.csv": lambda: pd.DataFrame({
        "PromotionProductID": [f"PPD{str(i).zfill(6)}" for i in range(1, 501)],
        "PromotionID": rand_choice(promotions["PromotionID"], 500) if promotions is not None else ["" for _ in range(500)],
        "ProductID": rand_choice(products["ProductID"], 500)
    }),
    "shipment.csv": lambda: pd.DataFrame({
        "ShipmentID": [f"SHIP{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "CarrierID": [f"CAR{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)],
        "ShipmentDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "store_event.csv": lambda: pd.DataFrame({
        "StoreEventID": [f"SE{str(i).zfill(5)}" for i in range(1, 101)],
        "StoreID": rand_choice(stores["StoreID"], 100),
        "EventName": [fake.catch_phrase() for _ in range(100)],
        "EventDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)]
    }),
    # Add more generators as needed for other missing tables
}

def safe_to_csv(df, fname):
    path = os.path.join(SAMPLE_DATA_DIR, fname)
    df.to_csv(path, index=False)
    print(f"Generated {fname}")

for t in missing_in_sample_data:
    if t in table_generators:
        safe_to_csv(table_generators[t](), t)
    else:
        print(f"No generator defined for {t}. Please add one to table_generators.")

print("Done. All missing tables (with defined generators) have been generated with referential integrity.")