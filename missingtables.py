import os

# List all expected tables (update this list as needed for your project)
expected_tables = [
    "customer.csv",
    "product.csv",
    "store.csv",
    "advertising_channel.csv",
    "online_order_aligned.csv",
    "order_lines.csv",
    "order_feedback.csv",
    "customer_support_ticket.csv",
    "promotion.csv",
    "promotion_redemption.csv",
    "order_return.csv",
    "store_staff.csv",
    "store_hours.csv",
    "inventory.csv",
    "financial_transactions.csv",
    "restock_order.csv",
    "gift_card.csv",
    "gift_card_transaction.csv",
    "inventory_costing.csv",
    "inventory_movement.csv",
    "cart_abandonment.csv",
    "abandoned_cart.csv",
    "coupon.csv",
    "coupon_redemption.csv",
    "product_review.csv",
    "customer_review.csv",
    "order_review.csv",
    "review.csv",
    "customer_feedback_by_product.csv",
    "customer_service_interaction.csv",
    "employee.csv",
    "employee_attendance.csv",
    "shift_schedule.csv",
    "subscription_plan.csv",
    "customer_subscription.csv",
    "return_reason.csv"
    # Add any other expected tables here
]

DATA_DIR = "sample_data"
existing_sample_data = set(f for f in os.listdir(DATA_DIR) if f.endswith('.csv'))
existing_root = set(f for f in os.listdir('.') if f.endswith('.csv'))

missing_in_sample_data = [t for t in expected_tables if t not in existing_sample_data]
missing_everywhere = [t for t in expected_tables if t not in existing_sample_data and t not in existing_root]

print("Missing tables in sample_data:")
for t in missing_in_sample_data:
    print(f"  {t}")

print("\nMissing tables everywhere (not in sample_data or project root):")
for t in missing_everywhere:
    print(f"  {t}")

if not missing_in_sample_data:
    print("\nAll expected tables are present in sample_data.")
if not missing_everywhere:
    print("\nAll expected tables are present in either sample_data or project root.")