import os
import pandas as pd

DATA_DIR = "sample_data"

# Define relationships as (child_file, child_col, parent_file, parent_col)
RELATIONSHIPS = [
    # Example relationships, update/add as needed for your schema
    ("order_lines.csv", "OrderID", "online_order_aligned.csv", "OnlineOrderID"),
    ("order_lines.csv", "ProductID", "product.csv", "ProductID"),
    ("online_order_aligned.csv", "CustomerID", "customer.csv", "CustomerID"),
    ("order_feedback.csv", "OrderID", "order_lines.csv", "OrderID"),
    ("product_review.csv", "ProductID", "product.csv", "ProductID"),
    ("product_review.csv", "CustomerID", "customer.csv", "CustomerID"),
    ("customer_review.csv", "CustomerID", "customer.csv", "CustomerID"),
    ("order_review.csv", "OrderID", "online_order_aligned.csv", "OnlineOrderID"),
    ("coupon_redemption.csv", "CouponID", "coupon.csv", "CouponID"),
    ("coupon_redemption.csv", "CustomerID", "customer.csv", "CustomerID"),
    ("customer_feedback_by_product.csv", "CustomerID", "customer.csv", "CustomerID"),
    ("customer_feedback_by_product.csv", "ProductID", "product.csv", "ProductID"),
    ("customer_service_interaction.csv", "CustomerID", "customer.csv", "CustomerID"),
    ("employee_attendance.csv", "EmployeeID", "employee.csv", "EmployeeID"),
    ("shift_schedule.csv", "EmployeeID", "employee.csv", "EmployeeID"),
    ("customer_subscription.csv", "CustomerID", "customer.csv", "CustomerID"),
    ("customer_subscription.csv", "PlanID", "subscription_plan.csv", "PlanID"),
    # Add more relationships as needed
]

def validate_fk(child_file, child_col, parent_file, parent_col):
    child_path = os.path.join(DATA_DIR, child_file)
    parent_path = os.path.join(DATA_DIR, parent_file)
    if not os.path.exists(child_path) or not os.path.exists(parent_path):
        print(f"Skipping {child_file} or {parent_file}: file not found.")
        return
    child_df = pd.read_csv(child_path, usecols=[child_col])
    parent_df = pd.read_csv(parent_path, usecols=[parent_col])
    missing = ~child_df[child_col].isin(parent_df[parent_col])
    if missing.any():
        print(f"[FAIL] {child_file}.{child_col} has {missing.sum()} values not found in {parent_file}.{parent_col}")
    else:
        print(f"[OK] {child_file}.{child_col} is valid against {parent_file}.{parent_col}")

if __name__ == "__main__":
    print("Validating referential integrity across sample_data...")
    for rel in RELATIONSHIPS:
        validate_fk(*rel)
    print("Validation complete.")