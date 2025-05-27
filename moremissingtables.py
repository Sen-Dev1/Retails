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


existing_tables = set(f for f in os.listdir(DATA_DIR) if f.endswith('.csv'))
missing_tables = [t for t in required_tables if t not in existing_tables]
print("Missing tables to generate:", missing_tables)

for t in missing_tables:
    if t in table_generators:
        safe_to_csv(table_generators[t](), t)
    else:
        print(f"No generator defined for {t}. Please add one to table_generators.")

def safe_to_csv(df, fname):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        df.to_csv(path, index=False)
        print(f"Generated {fname}")

def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if os.path.exists(path):
        return pd.read_csv(path)
    else:
        return None        
    

def safe_to_csv(df, fname):
    path = os.path.join(DATA_DIR, fname)
    df.to_csv(path, index=False)
    print(f"Generated {fname}")





print("Done. All missing tables (with defined generators) have been generated with referential integrity.")
customers = load_csv("customer.csv")
products = load_csv("product.csv")
stores = load_csv("store.csv")
orders = load_csv("online_order_aligned.csv")
employees = load_csv("employee.csv")
channels = load_csv("advertising_channel.csv")
promotions = load_csv("promotion.csv")
order_lines_final = load_csv("order_lines.csv")
refund_transaction = load_csv("refund_transaction.csv")
product_restock_threshold = load_csv("product_restock_threshold.csv")
product_category_assignment = load_csv("product_category_assignment.csv")
marketing_campaign_performance = load_csv("marketing_campaign_performance.csv")
online_order = load_csv("online_order.csv")
campaign_performance = load_csv("campaign_performance.csv")
advertising_channel_ref = load_csv("advertising_channel_ref.csv")
abandoned_checkout = load_csv("abandoned_checkout.csv")
product_question = load_csv("product_question.csv")
discount_code = load_csv("discount_code.csv")
product_view = load_csv("product_view.csv")
inventory_adjustment = load_csv("inventory_adjustment.csv")
loyalty_program = load_csv("loyalty_program.csv")
loyalty_reward = load_csv("loyalty_reward.csv")
return_request = load_csv("return_request.csv")
loyalty_transaction = load_csv("loyalty_transaction.csv")
delivery = load_csv("delivery.csv")
product_answer = load_csv("product_answer.csv")
store_feedback = load_csv("store_feedback.csv")
loyalty_points_transaction = load_csv("loyalty_points_transaction.csv")
shipment_tracking = load_csv("shipment_tracking.csv")
store_event = load_csv("store_event.csv")
customer_aligned = load_csv("customer_aligned.csv")
store_inventory_audit = load_csv("store_inventory_audit.csv")
store_inventory = load_csv("store_inventory.csv")
product_category = load_csv("product_category.csv")
returns_processing = load_csv("returns_processing.csv")
affiliate_referral = load_csv("affiliate_referral.csv")
shipment = load_csv("shipment.csv")
campaign_response = load_csv("campaign_response.csv")
browsing_history = load_csv("browsing_history.csv")
order_shipment = load_csv("order_shipment.csv")
customer_loyalty = load_csv("customer_loyalty.csv")
customer_satisfaction = load_csv("customer_satisfaction.csv")
delivery_address = load_csv("delivery_address.csv")
advertising_spend = load_csv("advertising_spend.csv")
customer_coupon = load_csv("customer_coupon.csv")
payment_method = load_csv("payment_method.csv")
fraud_alert = load_csv("fraud_alert.csv")
product_return = load_csv("product_return.csv")
shopping_cart = load_csv("shopping_cart.csv")
supplier = load_csv("supplier.csv")
product_promotion = load_csv("product_promotion.csv")
delivery_schedule = load_csv("delivery_schedule.csv")
employee_schedule = load_csv("employee_schedule.csv")
promotion_product = load_csv("promotion_product.csv")
sales_target = load_csv("sales_target.csv")
inventory_audit = load_csv("inventory_audit.csv")
delivery_exception = load_csv("delivery_exception.csv")
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

    "order_lines_final.csv": lambda: pd.DataFrame({
        "OrderLineFinalID": [f"OLF{str(i).zfill(7)}" for i in range(1, 2001)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 2000),
        "ProductID": rand_choice(products["ProductID"], 2000),
        "Quantity": np.random.randint(1, 5, 2000),
        "UnitPrice": rand_choice(products["UnitPrice"], 2000)
    }),
    "refund_transaction.csv": lambda: pd.DataFrame({
        "RefundTransactionID": [f"RT{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "RefundAmount": np.random.uniform(5, 500, 500).round(2),
        "RefundDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "product_restock_threshold.csv": lambda: pd.DataFrame({
        "RestockThresholdID": [f"PRT{str(i).zfill(5)}" for i in range(1, 501)],
        "ProductID": rand_choice(products["ProductID"], 500),
        "StoreID": rand_choice(stores["StoreID"], 500),
        "Threshold": np.random.randint(5, 50, 500)
    }),
    "product_category_assignment.csv": lambda: pd.DataFrame({
        "AssignmentID": [f"PCA{str(i).zfill(6)}" for i in range(1, 1001)],
        "ProductID": rand_choice(products["ProductID"], 1000),
        "CategoryID": [f"CAT{str(i).zfill(3)}" for i in np.random.randint(1, 21, 1000)]
    }),
    "marketing_campaign_performance.csv": lambda: pd.DataFrame({
        "PerformanceID": [f"MCP{str(i).zfill(5)}" for i in range(1, 101)],
        "CampaignID": [f"MC{str(i).zfill(5)}" for i in np.random.randint(1, 101, 100)],
        "Impressions": np.random.randint(1000, 100000, 100),
        "Clicks": np.random.randint(100, 10000, 100),
        "Conversions": np.random.randint(10, 1000, 100)
    }),
    "online_order.csv": lambda: pd.DataFrame({
        "OnlineOrderID": [f"ORD{str(i).zfill(6)}" for i in range(1, 2001)],
        "CustomerID": rand_choice(customers["CustomerID"], 2000),
        "StoreID": rand_choice(stores["StoreID"], 2000),
        "OrderDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(2000)],
        "TotalAmount": np.random.uniform(10, 1000, 2000).round(2)
    }),
    "campaign_performance.csv": lambda: pd.DataFrame({
        "CampaignPerformanceID": [f"CP{str(i).zfill(5)}" for i in range(1, 101)],
        "CampaignID": [f"MC{str(i).zfill(5)}" for i in np.random.randint(1, 101, 100)],
        "Spend": np.random.uniform(1000, 10000, 100).round(2),
        "Revenue": np.random.uniform(2000, 20000, 100).round(2)
    }),
    "advertising_channel_ref.csv": lambda: pd.DataFrame({
        "ChannelRefID": [f"ACR{str(i).zfill(4)}" for i in range(1, 21)],
        "ChannelID": rand_choice(channels["ChannelID"], 20),
        "Description": [fake.sentence() for _ in range(20)]
    }),
    "abandoned_checkout.csv": lambda: pd.DataFrame({
        "AbandonedCheckoutID": [f"AC{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "CartID": [f"CART{str(i).zfill(6)}" for i in np.random.randint(1, 4001, 500)],
        "AbandonDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "product_question.csv": lambda: pd.DataFrame({
        "QuestionID": [f"PQ{str(i).zfill(6)}" for i in range(1, 501)],
        "ProductID": rand_choice(products["ProductID"], 500),
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "QuestionText": [fake.sentence() for _ in range(500)],
        "DateAsked": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "discount_code.csv": lambda: pd.DataFrame({
        "DiscountCodeID": [f"DC{str(i).zfill(5)}" for i in range(1, 201)],
        "Code": [fake.bothify(text='????-#####') for _ in range(200)],
        "DiscountPercentage": np.random.randint(5, 50, 200),
        "ValidFrom": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(200)],
        "ValidTo": [fake.date_between(start_date='-1y', end_date='today') for _ in range(200)]
    }),
    "product_view.csv": lambda: pd.DataFrame({
        "ProductViewID": [f"PV{str(i).zfill(7)}" for i in range(1, 2001)],
        "ProductID": rand_choice(products["ProductID"], 2000),
        "CustomerID": rand_choice(customers["CustomerID"], 2000),
        "ViewDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(2000)]
    }),
    "inventory_adjustment.csv": lambda: pd.DataFrame({
        "AdjustmentID": [f"IA{str(i).zfill(6)}" for i in range(1, 501)],
        "ProductID": rand_choice(products["ProductID"], 500),
        "StoreID": rand_choice(stores["StoreID"], 500),
        "AdjustmentDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "QuantityChange": np.random.randint(-20, 20, 500)
    }),
    "loyalty_program.csv": lambda: pd.DataFrame({
        "LoyaltyProgramID": [f"LP{str(i).zfill(4)}" for i in range(1, 21)],
        "ProgramName": [fake.word().capitalize() for _ in range(20)],
        "StartDate": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(20)],
        "EndDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(20)]
    }),
    "loyalty_reward.csv": lambda: pd.DataFrame({
        "RewardID": [f"LR{str(i).zfill(5)}" for i in range(1, 201)],
        "LoyaltyProgramID": [f"LP{str(i).zfill(4)}" for i in np.random.randint(1, 21, 200)],
        "RewardDescription": [fake.sentence() for _ in range(200)],
        "PointsRequired": np.random.randint(100, 1000, 200)
    }),
    "return_request.csv": lambda: pd.DataFrame({
        "ReturnRequestID": [f"RRQ{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "RequestDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Reason": [fake.sentence() for _ in range(500)]
    }),
  

# ...existing code...

    "loyalty_transaction.csv": lambda: pd.DataFrame({
        "LoyaltyTransactionID": [f"LT{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "LoyaltyProgramID": [f"LP{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)],
        "Points": np.random.randint(10, 500, 500),
        "TransactionDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "delivery.csv": lambda: pd.DataFrame({
        "DeliveryID": [f"DEL{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "CarrierID": [f"CAR{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)],
        "DeliveryDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Status": np.random.choice(['Pending', 'Shipped', 'Delivered'], 500)
    }),
    "product_answer.csv": lambda: pd.DataFrame({
        "AnswerID": [f"PA{str(i).zfill(6)}" for i in range(1, 501)],
        "QuestionID": [f"PQ{str(i).zfill(6)}" for i in np.random.randint(1, 501, 500)],
        "EmployeeID": rand_choice(employees["EmployeeID"], 500),
        "AnswerText": [fake.sentence() for _ in range(500)],
        "DateAnswered": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "store_feedback.csv": lambda: pd.DataFrame({
        "StoreFeedbackID": [f"SF{str(i).zfill(6)}" for i in range(1, 501)],
        "StoreID": rand_choice(stores["StoreID"], 500),
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "FeedbackText": [fake.sentence() for _ in range(500)],
        "Date": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "loyalty_points_transaction.csv": lambda: pd.DataFrame({
        "PointsTransactionID": [f"LPT{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "LoyaltyProgramID": [f"LP{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)],
        "Points": np.random.randint(1, 100, 500),
        "TransactionDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "shipment_tracking.csv": lambda: pd.DataFrame({
        "ShipmentTrackingID": [f"ST{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "CarrierID": [f"CAR{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)],
        "Status": np.random.choice(['In Transit', 'Delivered', 'Delayed'], 500),
        "UpdateDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "store_event.csv": lambda: pd.DataFrame({
        "StoreEventID": [f"SE{str(i).zfill(5)}" for i in range(1, 101)],
        "StoreID": rand_choice(stores["StoreID"], 100),
        "EventName": [fake.catch_phrase() for _ in range(100)],
        "EventDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)]
    }),
    "customer_aligned.csv": lambda: pd.DataFrame({
        "CustomerAlignedID": [f"CA{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "AlignedGroup": [fake.word().capitalize() for _ in range(500)]
    }),
    "store_inventory_audit.csv": lambda: pd.DataFrame({
        "InventoryAuditID": [f"SIA{str(i).zfill(6)}" for i in range(1, 501)],
        "StoreID": rand_choice(stores["StoreID"], 500),
        "ProductID": rand_choice(products["ProductID"], 500),
        "AuditDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Quantity": np.random.randint(0, 200, 500)
    }),
    "store_inventory.csv": lambda: pd.DataFrame({
        "StoreInventoryID": [f"SI{str(i).zfill(6)}" for i in range(1, 501)],
        "StoreID": rand_choice(stores["StoreID"], 500),
        "ProductID": rand_choice(products["ProductID"], 500),
        "Quantity": np.random.randint(0, 200, 500)
    }),
    "product_category.csv": lambda: pd.DataFrame({
        "CategoryID": [f"CAT{str(i).zfill(3)}" for i in range(1, 21)],
        "CategoryName": [fake.word().capitalize() for _ in range(20)]
    }),
    "returns_processing.csv": lambda: pd.DataFrame({
        "ReturnsProcessingID": [f"RP{str(i).zfill(6)}" for i in range(1, 501)],
        "ReturnRequestID": [f"RRQ{str(i).zfill(6)}" for i in np.random.randint(1, 501, 500)],
        "ProcessedDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Status": np.random.choice(['Processed', 'Pending', 'Rejected'], 500)
    }),
    "affiliate_referral.csv": lambda: pd.DataFrame({
        "AffiliateReferralID": [f"AR{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "AffiliateCode": [fake.bothify(text='AFF-#####') for _ in range(500)],
        "ReferralDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "shipment.csv": lambda: pd.DataFrame({
        "ShipmentID": [f"SHIP{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "CarrierID": [f"CAR{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)],
        "ShipmentDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "campaign_response.csv": lambda: pd.DataFrame({
        "CampaignResponseID": [f"CR{str(i).zfill(6)}" for i in range(1, 501)],
        "CampaignID": [f"MC{str(i).zfill(5)}" for i in np.random.randint(1, 101, 500)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "ResponseDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "browsing_history.csv": lambda: pd.DataFrame({
        "BrowsingHistoryID": [f"BH{str(i).zfill(6)}" for i in range(1, 2001)],
        "CustomerID": rand_choice(customers["CustomerID"], 2000),
        "ProductID": rand_choice(products["ProductID"], 2000),
        "ViewDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(2000)]
    }),
    "order_shipment.csv": lambda: pd.DataFrame({
        "OrderShipmentID": [f"OS{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "ShipmentID": [f"SHIP{str(i).zfill(6)}" for i in np.random.randint(1, 501, 500)],
        "ShipmentDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
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
    "advertising_spend.csv": lambda: pd.DataFrame({
        "AdSpendID": [f"AS{str(i).zfill(6)}" for i in range(1, 201)],
        "ChannelID": rand_choice(channels["ChannelID"], 200),
        "SpendDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(200)],
        "Amount": np.random.uniform(100, 10000, 200).round(2)
    }),
    "customer_coupon.csv": lambda: pd.DataFrame({
        "CustomerCouponID": [f"CC{str(i).zfill(6)}" for i in range(1, 501)],
        "CustomerID": rand_choice(customers["CustomerID"], 500),
        "CouponID": [f"COUP{str(i).zfill(5)}" for i in np.random.randint(1, 201, 500)],
        "AssignedDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)]
    }),
    "payment_method.csv": lambda: pd.DataFrame({
        "PaymentMethodID": [f"PM{str(i).zfill(5)}" for i in range(1, 101)],
        "CustomerID": rand_choice(customers["CustomerID"], 100),
        "Method": np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Gift Card'], 100),
        "AddedDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(100)]
    }),
    "fraud_alert.csv": lambda: pd.DataFrame({
        "FraudAlertID": [f"FA{str(i).zfill(6)}" for i in range(1, 101)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 100),
        "CustomerID": rand_choice(customers["CustomerID"], 100),
        "AlertDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)],
        "Reason": [fake.sentence() for _ in range(100)]
    }),
    "product_return.csv": lambda: pd.DataFrame({
        "ProductReturnID": [f"PR{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "ProductID": rand_choice(products["ProductID"], 500),
        "ReturnDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Reason": [fake.sentence() for _ in range(500)]
    }),
    "shopping_cart.csv": lambda: pd.DataFrame({
        "CartID": [f"CART{str(i).zfill(6)}" for i in range(1, 1001)],
        "CustomerID": rand_choice(customers["CustomerID"], 1000),
        "CreatedDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(1000)]
    }),
    "supplier.csv": lambda: pd.DataFrame({
        "SupplierID": [f"SUP{str(i).zfill(4)}" for i in range(1, 61)],
        "SupplierName": [fake.company() for _ in range(60)],
        "ContactName": [fake.name() for _ in range(60)],
        "ContactEmail": [fake.email() for _ in range(60)]
    }),
    "product_promotion.csv": lambda: pd.DataFrame({
        "ProductPromotionID": [f"PP{str(i).zfill(6)}" for i in range(1, 501)],
        "ProductID": rand_choice(products["ProductID"], 500),
        "PromotionID": rand_choice(promotions["PromotionID"], 500) if promotions is not None else ["" for _ in range(500)],
        "StartDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "EndDate": [fake.date_between(start_date='today', end_date='+30d') for _ in range(500)]
    }),
    "delivery_schedule.csv": lambda: pd.DataFrame({
        "DeliveryScheduleID": [f"DS{str(i).zfill(6)}" for i in range(1, 501)],
        "OrderID": rand_choice(orders["OnlineOrderID"], 500),
        "ScheduledDate": [fake.date_between(start_date='today', end_date='+30d') for _ in range(500)],
        "CarrierID": [f"CAR{str(i).zfill(4)}" for i in np.random.randint(1, 21, 500)]
    }),
    "employee_schedule.csv": lambda: pd.DataFrame({
        "EmployeeScheduleID": [f"ES{str(i).zfill(6)}" for i in range(1, 501)],
        "EmployeeID": rand_choice(employees["EmployeeID"], 500),
        "ScheduleDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Shift": np.random.choice(['Morning', 'Afternoon', 'Evening'], 500)
    }),
    "promotion_product.csv": lambda: pd.DataFrame({
        "PromotionProductID": [f"PPD{str(i).zfill(6)}" for i in range(1, 501)],
        "PromotionID": rand_choice(promotions["PromotionID"], 500) if promotions is not None else ["" for _ in range(500)],
        "ProductID": rand_choice(products["ProductID"], 500)
    }),
    "sales_target.csv": lambda: pd.DataFrame({
        "SalesTargetID": [f"ST{str(i).zfill(6)}" for i in range(1, 101)],
        "StoreID": rand_choice(stores["StoreID"], 100),
        "TargetAmount": np.random.uniform(10000, 100000, 100).round(2),
        "TargetMonth": [fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m') for _ in range(100)]
    }),
    "inventory_audit.csv": lambda: pd.DataFrame({
        "InventoryAuditID": [f"IAU{str(i).zfill(6)}" for i in range(1, 501)],
        "StoreID": rand_choice(stores["StoreID"], 500),
        "ProductID": rand_choice(products["ProductID"], 500),
        "AuditDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(500)],
        "Quantity": np.random.randint(0, 200, 500)
    }),
    "delivery_exception.csv": lambda: pd.DataFrame({
        "DeliveryExceptionID": [f"DE{str(i).zfill(6)}" for i in range(1, 101)],
        "DeliveryID": [f"DEL{str(i).zfill(6)}" for i in np.random.randint(1, 501, 100)],
        "ExceptionDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(100)],
        "Reason": [fake.sentence() for _ in range(100)]
    })
}  # <-- Add this closing brace to end the dictionary
# End of table_generators dictionary

# ...existing code for safe_to_csv and for loop...



 # Add more generators for each missing table, always referencing existing sample_data tables for foreign key

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




# Add this line here:
print("Missing tables to generate:", missing_tables)

for t in missing_tables:
    if t in table_generators:
        safe_to_csv(table_generators[t](), t)
    else:
        print(f"No generator defined for {t}. Please add one to table_generators.")