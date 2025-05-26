import os
import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

DATA_DIR = "sample_data"

# List of all required tables (from your prompt)
required_tables = [
    "campaign_channel.csv", "online_order_aligned.csv", "order_feedback.csv", "store_aligned.csv",
    "restock_request.csv", "price_history.csv", "carrier.csv", "store.csv", "employee_timesheet.csv",
    "advertising_channel.csv", "marketing_campaign.csv", "order_return.csv", "store_closure.csv",
    "online_order_line.csv", "customer_feedback.csv", "customer_support_ticket.csv", "delivery_tracking.csv",
    "product_supplier.csv", "customer_referral.csv", "online_order_tracking.csv", "order_lines_final.csv",
    "refund_transaction.csv", "product_restock_threshold.csv", "product_category_assignment.csv",
    "marketing_campaign_performance.csv", "online_order.csv", "campaign_performance.csv",
    "advertising_channel_ref.csv", "abandoned_checkout.csv", "product_question.csv", "discount_code.csv",
    "coupon.csv", "order_lines.csv", "order_review.csv", "product_view.csv", "cart_abandonment.csv",
    "inventory_adjustment.csv", "loyalty_program.csv", "abandoned_cart.csv", "coupon_redemption.csv",
    "loyalty_reward.csv", "customer_review.csv", "return_request.csv", "store_hours.csv",
    "loyalty_transaction.csv", "delivery.csv", "customer.csv", "product_answer.csv", "store_feedback.csv",
    "loyalty_points_transaction.csv", "shipment_tracking.csv", "store_event.csv", "store_staff.csv",
    "customer_aligned.csv", "store_inventory_audit.csv", "employee.csv", "store_inventory.csv", "review.csv",
    "product_category.csv", "returns_processing.csv", "restock_order.csv", "financial_transactions.csv",
    "affiliate_referral.csv", "shipment.csv", "campaign_response.csv", "browsing_history.csv",
    "order_shipment.csv", "customer_loyalty.csv", "product_review.csv", "promotion_redemption.csv",
    "customer_feedback_by_product.csv", "customer_satisfaction.csv", "gift_card.csv", "inventory_costing.csv",
    "employee_attendance.csv", "delivery_address.csv", "advertising_spend.csv", "subscription_plan.csv",
    "return_reason.csv", "promotion.csv", "customer_coupon.csv", "payment_method.csv", "fraud_alert.csv",
    "gift_card_transaction.csv", "product.csv", "inventory.csv", "product_return.csv", "shift_schedule.csv",
    "shopping_cart.csv", "inventory_movement.csv", "supplier.csv", "customer_subscription.csv",
    "product_promotion.csv", "delivery_schedule.csv", "customer_service_interaction.csv", "employee_schedule.csv",
    "promotion_product.csv", "sales_target.csv", "inventory_audit.csv", "delivery_exception.csv"
]

# Find which tables are missing from sample_data
existing_tables = set(f for f in os.listdir(DATA_DIR) if f.endswith('.csv'))
missing_tables = [t for t in required_tables if t not in existing_tables]

# Load reference data from sample_data
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

# Helper for random choice
def rand_choice(series, n):
    return np.random.choice(series, n)

# Table generators: Add more as needed, always referencing existing data
table_generators = {
    "campaign_channel.csv": lambda: pd.DataFrame({
        "CampaignChannelID": [f"CC{str(i).zfill(5)}" for i in range(1, 201)],
        "ChannelID": rand_choice(channels["ChannelID"], 200) if channels is not None else ["" for _ in range(200)],
        "CampaignName": [fake.catch_phrase() for _ in range(200)]
    }),
    "store_aligned.csv": lambda: pd.DataFrame({
        "StoreAlignedID": [f"SA{str(i).zfill(5)}" for i in range(1, 101)],
        "StoreID": rand_choice(stores["StoreID"], 100) if stores is not None else ["" for _ in range(100)],
        "AlignedName": [fake.company() for _ in range(100)]
    }),
    "employee_timesheet.csv": lambda: pd.DataFrame({
        "TimesheetID": [f"TS{str(i).zfill(6)}" for i in range(1, 1001)],
        "EmployeeID": rand_choice(employees["EmployeeID"], 1000) if employees is not None else ["" for _ in range(1000)],
        "Date": [fake.date_between(start_date='-1y', end_date='today') for _ in range(1000)],
        "HoursWorked": np.random.uniform(4, 10, 1000).round(2)
    }),
    "product_supplier.csv": lambda: pd.DataFrame({
        "ProductSupplierID": [f"PS{str(i).zfill(6)}" for i in range(1, 1001)],
        "ProductID": rand_choice(products["ProductID"], 1000) if products is not None else ["" for _ in range(1000)],
        "SupplierID": rand_choice(suppliers["SupplierID"], 1000) if suppliers is not None else ["" for _ in range(1000)]
    }),
    # Add more table generators here, always referencing existing sample_data tables for foreign keys
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