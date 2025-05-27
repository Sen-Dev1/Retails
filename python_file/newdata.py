import pandas as pd
import numpy as np
import os
from faker import Faker

fake = Faker()
np.random.seed(42)

# Parameters
NUM_CUSTOMERS = 3000
NUM_PRODUCTS = 800
NUM_ORDERS = 20000
NUM_ORDER_LINES = 40000
NUM_STORES = 80
NUM_CHANNELS = 20
NUM_FEEDBACK = 40000
NUM_TICKETS = 4000
NUM_PROMOS = 40
NUM_PROMO_REDEMPTIONS = 2000
NUM_RETURNS = 2000
NUM_SUPPLIERS = 60
NUM_RESTOCK_ORDERS = 1000
NUM_INVENTORY = 2000
NUM_STORE_STAFF = 600
NUM_STORE_HOURS = 700
NUM_GIFTCARDS = 1000
NUM_GIFTCARD_TX = 2000
NUM_INVENTORY_COSTING = 1000
NUM_INVENTORY_MOVEMENT = 2000
NUM_CARTS = 4000
NUM_CART_ABANDON = 1000
NUM_ABANDONED_CART = 1000
NUM_COUPONS = 200
NUM_COUPON_REDEMPTION = 1000
NUM_PRODUCT_REVIEW = 4000
NUM_CUSTOMER_REVIEW = 4000
NUM_ORDER_REVIEW = 4000
NUM_REVIEW = 4000
NUM_CUSTOMER_FEEDBACK_BY_PRODUCT = 4000
NUM_CUSTOMER_SERVICE_INTERACTION = 4000
NUM_EMPLOYEE = 200
NUM_EMPLOYEE_ATTENDANCE = 2000
NUM_SHIFT_SCHEDULE = 600
NUM_SUBSCRIPTION_PLAN = 20
NUM_CUSTOMER_SUBSCRIPTION = 400
NUM_RETURN_REASON = 20
NUM_PRODUCT_SUPPLIER = 1000
NUM_SUPPLIER = 60
NUM_CAMPAIGN_CHANNEL = 40
NUM_CAMPAIGN_RESPONSE = 2000
NUM_ONLINE_ORDER_TRACKING = 2000
NUM_SHIPMENT_TRACKING = 2000
NUM_DELIVERY_TRACKING = 2000
NUM_ORDER_SHIPMENT = 2000
NUM_PRODUCT_CATEGORY_ASSIGNMENT = 1000
NUM_PRODUCT_CATEGORY = 40
NUM_PROMOTION_PRODUCT = 200
NUM_STORE_INVENTORY = 1000
NUM_STORE_INVENTORY_AUDIT = 1000
NUM_DELIVERY_SCHEDULE = 200
NUM_SHOPPING_CART = 4000
NUM_CUSTOMER_SATISFACTION = 2000

os.makedirs("sample_data", exist_ok=True)

# Customers
customers = pd.DataFrame({
    "CustomerID": [f"CUST{str(i).zfill(5)}" for i in range(1, NUM_CUSTOMERS+1)],
    "FirstName": [fake.first_name() for _ in range(NUM_CUSTOMERS)],
    "LastName": [fake.last_name() for _ in range(NUM_CUSTOMERS)],
    "Email": [fake.email() for _ in range(NUM_CUSTOMERS)],
    "Gender": np.random.choice(['M', 'F'], NUM_CUSTOMERS),
    "BirthDate": [fake.date_of_birth(minimum_age=18, maximum_age=80) for _ in range(NUM_CUSTOMERS)],
    "City": [fake.city() for _ in range(NUM_CUSTOMERS)],
    "State": [fake.state_abbr() for _ in range(NUM_CUSTOMERS)],
    "Country": [fake.country() for _ in range(NUM_CUSTOMERS)],
    "SignupDate": [fake.date_between(start_date='-5y', end_date='today') for _ in range(NUM_CUSTOMERS)]
})
customers.to_csv("sample_data/customer.csv", index=False)

# Products
products = pd.DataFrame({
    "ProductID": [f"PROD{str(i).zfill(5)}" for i in range(1, NUM_PRODUCTS+1)],
    "ProductName": [fake.word().capitalize() for _ in range(NUM_PRODUCTS)],
    "Category": np.random.choice(['Electronics', 'Clothing', 'Home', 'Toys', 'Books'], NUM_PRODUCTS),
    "UnitPrice": np.random.uniform(5, 500, NUM_PRODUCTS).round(2)
})
products.to_csv("sample_data/product.csv", index=False)

# Stores
stores = pd.DataFrame({
    "StoreID": [f"STORE{str(i).zfill(3)}" for i in range(1, NUM_STORES+1)],
    "City": [fake.city() for _ in range(NUM_STORES)],
    "State": [fake.state_abbr() for _ in range(NUM_STORES)],
    "Country": [fake.country() for _ in range(NUM_STORES)]
})
stores.to_csv("sample_data/store.csv", index=False)

# Advertising Channels
channels = pd.DataFrame({
    "ChannelID": [f"CHAN{str(i).zfill(3)}" for i in range(1, NUM_CHANNELS+1)],
    "ChannelName": [fake.company() for _ in range(NUM_CHANNELS)]
})
channels.to_csv("sample_data/advertising_channel.csv", index=False)

# Online Orders
online_orders = pd.DataFrame({
    "OnlineOrderID": [f"ORD{str(i).zfill(6)}" for i in range(1, NUM_ORDERS+1)],
    "CustomerID": np.random.choice(customers["CustomerID"], NUM_ORDERS),
    "ProductID": np.random.choice(products["ProductID"], NUM_ORDERS),
    "ChannelID": np.random.choice(channels["ChannelID"], NUM_ORDERS),
    "StoreID": np.random.choice(stores["StoreID"], NUM_ORDERS),
    "OrderDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_ORDERS)]
})
online_orders.to_csv("sample_data/online_order_aligned.csv", index=False)

# Order Lines
order_lines = pd.DataFrame({
    "OrderLineID": [f"OL{str(i).zfill(7)}" for i in range(1, NUM_ORDER_LINES+1)],
    "OrderID": np.random.choice(online_orders["OnlineOrderID"], NUM_ORDER_LINES),
    "ProductID": np.random.choice(products["ProductID"], NUM_ORDER_LINES),
    "Quantity": np.random.randint(1, 5, NUM_ORDER_LINES),
    "UnitPrice": np.random.choice(products["UnitPrice"], NUM_ORDER_LINES)
})
order_lines.to_csv("sample_data/order_lines.csv", index=False)

# Order Feedback
order_feedback = pd.DataFrame({
    "FeedbackID": [f"FB{str(i).zfill(7)}" for i in range(1, NUM_FEEDBACK+1)],
    "OrderID": np.random.choice(order_lines["OrderID"], NUM_FEEDBACK),
    "Rating": np.random.randint(1, 6, NUM_FEEDBACK),
    "Comment": [fake.sentence() for _ in range(NUM_FEEDBACK)]
})
order_feedback.to_csv("sample_data/order_feedback.csv", index=False)

# Customer Support Ticket
support_tickets = pd.DataFrame({
    "TicketID": [f"TIC{str(i).zfill(7)}" for i in range(1, NUM_TICKETS+1)],
    "CustomerID": np.random.choice(customers["CustomerID"], NUM_TICKETS),
    "Status": np.random.choice(['Open', 'Resolved', 'Pending'], NUM_TICKETS),
    "CreatedDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_TICKETS)]
})
support_tickets.to_csv("sample_data/customer_support_ticket.csv", index=False)

# Promotions
promotions = pd.DataFrame({
    "PromotionID": [f"PROMO{str(i).zfill(4)}" for i in range(1, NUM_PROMOS+1)],
    "PromotionName": [fake.catch_phrase() for _ in range(NUM_PROMOS)]
})
promotions.to_csv("sample_data/promotion.csv", index=False)

# Promotion Redemption
promotion_redemption = pd.DataFrame({
    "RedemptionID": [f"RED{str(i).zfill(6)}" for i in range(1, NUM_PROMO_REDEMPTIONS+1)],
    "PromotionID": np.random.choice(promotions["PromotionID"], NUM_PROMO_REDEMPTIONS),
    "OrderID": np.random.choice(online_orders["OnlineOrderID"], NUM_PROMO_REDEMPTIONS),
    "RedemptionDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_PROMO_REDEMPTIONS)]
})
promotion_redemption.to_csv("sample_data/promotion_redemption.csv", index=False)

# Order Return
order_return = pd.DataFrame({
    "ReturnID": [f"RET{str(i).zfill(6)}" for i in range(1, NUM_RETURNS+1)],
    "OrderID": np.random.choice(online_orders["OnlineOrderID"], NUM_RETURNS),
    "RefundIssued": np.random.choice([0, 1], NUM_RETURNS),
    "ReturnDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_RETURNS)]
})
order_return.to_csv("sample_data/order_return.csv", index=False)

# Continue for all other tables in your project, following the above pattern.
# For each table, ensure you use the correct relationships and foreign keys.

# Example for a few more:
# Store Staff
store_staff = pd.DataFrame({
    "StaffID": [f"STAFF{str(i).zfill(5)}" for i in range(1, NUM_STORE_STAFF+1)],
    "StoreID": np.random.choice(stores["StoreID"], NUM_STORE_STAFF),
    "FirstName": [fake.first_name() for _ in range(NUM_STORE_STAFF)],
    "LastName": [fake.last_name() for _ in range(NUM_STORE_STAFF)],
    "Role": np.random.choice(['Manager', 'Cashier', 'Stocker', 'Sales'], NUM_STORE_STAFF)
})
store_staff.to_csv("sample_data/store_staff.csv", index=False)

# Store Hours
store_hours = pd.DataFrame({
    "StoreID": np.random.choice(stores["StoreID"], NUM_STORE_HOURS),
    "DayOfWeek": np.random.choice(['Mon','Tue','Wed','Thu','Fri','Sat','Sun'], NUM_STORE_HOURS),
    "OpenTime": [fake.time(pattern="%H:%M") for _ in range(NUM_STORE_HOURS)],
    "CloseTime": [fake.time(pattern="%H:%M") for _ in range(NUM_STORE_HOURS)]
})
store_hours.to_csv("sample_data/store_hours.csv", index=False)

# Inventory
inventory = pd.DataFrame({
    "InventoryID": [f"INV{str(i).zfill(6)}" for i in range(1, NUM_INVENTORY+1)],
    "ProductID": np.random.choice(products["ProductID"], NUM_INVENTORY),
    "StoreID": np.random.choice(stores["StoreID"], NUM_INVENTORY),
    "Quantity": np.random.randint(0, 100, NUM_INVENTORY)
})
inventory.to_csv("sample_data/inventory.csv", index=False)

# Add all other tables as needed, using the same approach.
# For each, ensure you use the correct relationships and foreign keys.

print("All sample data generated in the 'sample_data' directory.")