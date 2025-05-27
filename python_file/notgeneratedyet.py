import pandas as pd
import numpy as np
import os
from faker import Faker

fake = Faker()
np.random.seed(42)

DATA_DIR = "sample_data"

# Load already generated tables for reference keys
customers = pd.read_csv(f"{DATA_DIR}/customer.csv")
products = pd.read_csv(f"{DATA_DIR}/product.csv")
stores = pd.read_csv(f"{DATA_DIR}/store.csv")
channels = pd.read_csv(f"{DATA_DIR}/advertising_channel.csv")
online_orders = pd.read_csv(f"{DATA_DIR}/online_order_aligned.csv")
order_lines = pd.read_csv(f"{DATA_DIR}/order_lines.csv")
promotions = pd.read_csv(f"{DATA_DIR}/promotion.csv")

def rand_choice(series, n):
    return np.random.choice(series, n)

# Only generate if file does not exist
def safe_to_csv(df, fname):
    path = os.path.join(DATA_DIR, fname)
    if not os.path.exists(path):
        df.to_csv(path, index=False)
        print(f"Generated {fname}")

# Example: Generate coupon.csv
NUM_COUPONS = 200
coupons = pd.DataFrame({
    "CouponID": [f"COUP{str(i).zfill(5)}" for i in range(1, NUM_COUPONS+1)],
    "DiscountPercentage": np.random.randint(5, 50, NUM_COUPONS),
    "ValidFrom": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(NUM_COUPONS)],
    "ValidTo": [fake.date_between(start_date='-1y', end_date='today') for _ in range(NUM_COUPONS)]
})
safe_to_csv(coupons, "coupon.csv")

# coupon_redemption.csv
NUM_COUPON_REDEMPTION = 1000
coupon_redemption = pd.DataFrame({
    "RedemptionID": [f"CR{str(i).zfill(6)}" for i in range(1, NUM_COUPON_REDEMPTION+1)],
    "CouponID": rand_choice(coupons["CouponID"], NUM_COUPON_REDEMPTION),
    "CustomerID": rand_choice(customers["CustomerID"], NUM_COUPON_REDEMPTION),
    "RedemptionDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_COUPON_REDEMPTION)]
})
safe_to_csv(coupon_redemption, "coupon_redemption.csv")

# product_review.csv
NUM_PRODUCT_REVIEW = 4000
product_review = pd.DataFrame({
    "ProductReviewID": [f"PR{str(i).zfill(6)}" for i in range(1, NUM_PRODUCT_REVIEW+1)],
    "ProductID": rand_choice(products["ProductID"], NUM_PRODUCT_REVIEW),
    "CustomerID": rand_choice(customers["CustomerID"], NUM_PRODUCT_REVIEW),
    "Rating": np.random.randint(1, 6, NUM_PRODUCT_REVIEW),
    "ReviewText": [fake.sentence() for _ in range(NUM_PRODUCT_REVIEW)]
})
safe_to_csv(product_review, "product_review.csv")

# customer_review.csv
NUM_CUSTOMER_REVIEW = 4000
customer_review = pd.DataFrame({
    "CustomerReviewID": [f"CRV{str(i).zfill(6)}" for i in range(1, NUM_CUSTOMER_REVIEW+1)],
    "CustomerID": rand_choice(customers["CustomerID"], NUM_CUSTOMER_REVIEW),
    "Rating": np.random.randint(1, 6, NUM_CUSTOMER_REVIEW),
    "ReviewText": [fake.sentence() for _ in range(NUM_CUSTOMER_REVIEW)]
})
safe_to_csv(customer_review, "customer_review.csv")

# order_review.csv
NUM_ORDER_REVIEW = 4000
order_review = pd.DataFrame({
    "OrderReviewID": [f"ORV{str(i).zfill(6)}" for i in range(1, NUM_ORDER_REVIEW+1)],
    "OrderID": rand_choice(online_orders["OnlineOrderID"], NUM_ORDER_REVIEW),
    "Rating": np.random.randint(1, 6, NUM_ORDER_REVIEW),
    "ReviewText": [fake.sentence() for _ in range(NUM_ORDER_REVIEW)]
})
safe_to_csv(order_review, "order_review.csv")

# review.csv (generic)
NUM_REVIEW = 4000
review = pd.DataFrame({
    "ReviewID": [f"REV{str(i).zfill(6)}" for i in range(1, NUM_REVIEW+1)],
    "Rating": np.random.randint(1, 6, NUM_REVIEW),
    "ReviewText": [fake.sentence() for _ in range(NUM_REVIEW)]
})
safe_to_csv(review, "review.csv")

# customer_feedback_by_product.csv
NUM_CUSTOMER_FEEDBACK_BY_PRODUCT = 4000
customer_feedback_by_product = pd.DataFrame({
    "FeedbackID": [f"CFBP{str(i).zfill(6)}" for i in range(1, NUM_CUSTOMER_FEEDBACK_BY_PRODUCT+1)],
    "CustomerID": rand_choice(customers["CustomerID"], NUM_CUSTOMER_FEEDBACK_BY_PRODUCT),
    "ProductID": rand_choice(products["ProductID"], NUM_CUSTOMER_FEEDBACK_BY_PRODUCT),
    "Rating": np.random.randint(1, 6, NUM_CUSTOMER_FEEDBACK_BY_PRODUCT),
    "DateCreated": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_CUSTOMER_FEEDBACK_BY_PRODUCT)]
})
safe_to_csv(customer_feedback_by_product, "customer_feedback_by_product.csv")

# customer_service_interaction.csv
NUM_CUSTOMER_SERVICE_INTERACTION = 4000
customer_service_interaction = pd.DataFrame({
    "InteractionID": [f"CSI{str(i).zfill(6)}" for i in range(1, NUM_CUSTOMER_SERVICE_INTERACTION+1)],
    "CustomerID": rand_choice(customers["CustomerID"], NUM_CUSTOMER_SERVICE_INTERACTION),
    "SatisfactionRating": np.random.randint(1, 6, NUM_CUSTOMER_SERVICE_INTERACTION),
    "DateCreated": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_CUSTOMER_SERVICE_INTERACTION)]
})
safe_to_csv(customer_service_interaction, "customer_service_interaction.csv")

# employee.csv
NUM_EMPLOYEE = 200
employee = pd.DataFrame({
    "EmployeeID": [f"EMP{str(i).zfill(5)}" for i in range(1, NUM_EMPLOYEE+1)],
    "FirstName": [fake.first_name() for _ in range(NUM_EMPLOYEE)],
    "LastName": [fake.last_name() for _ in range(NUM_EMPLOYEE)],
    "Role": np.random.choice(['Manager', 'Cashier', 'Stocker', 'Sales'], NUM_EMPLOYEE)
})
safe_to_csv(employee, "employee.csv")

# employee_attendance.csv
NUM_EMPLOYEE_ATTENDANCE = 2000
employee_attendance = pd.DataFrame({
    "AttendanceID": [f"EA{str(i).zfill(6)}" for i in range(1, NUM_EMPLOYEE_ATTENDANCE+1)],
    "EmployeeID": rand_choice(employee["EmployeeID"], NUM_EMPLOYEE_ATTENDANCE),
    "Date": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_EMPLOYEE_ATTENDANCE)],
    "Status": np.random.choice(['Present', 'Absent', 'Late'], NUM_EMPLOYEE_ATTENDANCE)
})
safe_to_csv(employee_attendance, "employee_attendance.csv")

# shift_schedule.csv
NUM_SHIFT_SCHEDULE = 600
shift_schedule = pd.DataFrame({
    "ShiftID": [f"SHIFT{str(i).zfill(5)}" for i in range(1, NUM_SHIFT_SCHEDULE+1)],
    "EmployeeID": rand_choice(employee["EmployeeID"], NUM_SHIFT_SCHEDULE),
    "ShiftDate": [fake.date_between(start_date='-2y', end_date='today') for _ in range(NUM_SHIFT_SCHEDULE)],
    "Shift": np.random.choice(['Morning', 'Afternoon', 'Evening'], NUM_SHIFT_SCHEDULE)
})
safe_to_csv(shift_schedule, "shift_schedule.csv")

# subscription_plan.csv
NUM_SUBSCRIPTION_PLAN = 20
subscription_plan = pd.DataFrame({
    "PlanID": [f"PLAN{str(i).zfill(3)}" for i in range(1, NUM_SUBSCRIPTION_PLAN+1)],
    "PlanName": [fake.word().capitalize() for _ in range(NUM_SUBSCRIPTION_PLAN)],
    "MonthlyFee": np.random.uniform(5, 100, NUM_SUBSCRIPTION_PLAN).round(2)
})
safe_to_csv(subscription_plan, "subscription_plan.csv")

# customer_subscription.csv
NUM_CUSTOMER_SUBSCRIPTION = 400
customer_subscription = pd.DataFrame({
    "SubscriptionID": [f"SUB{str(i).zfill(5)}" for i in range(1, NUM_CUSTOMER_SUBSCRIPTION+1)],
    "CustomerID": rand_choice(customers["CustomerID"], NUM_CUSTOMER_SUBSCRIPTION),
    "PlanID": rand_choice(subscription_plan["PlanID"], NUM_CUSTOMER_SUBSCRIPTION),
    "StartDate": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(NUM_CUSTOMER_SUBSCRIPTION)],
    "EndDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(NUM_CUSTOMER_SUBSCRIPTION)]
})
safe_to_csv(customer_subscription, "customer_subscription.csv")

# return_reason.csv
NUM_RETURN_REASON = 20
return_reason = pd.DataFrame({
    "ReasonID": [f"RR{str(i).zfill(3)}" for i in range(1, NUM_RETURN_REASON+1)],
    "ReasonText": [fake.sentence() for _ in range(NUM_RETURN_REASON)]
})
safe_to_csv(return_reason, "return_reason.csv")

# Add more tables as needed, following the same pattern and referencing keys from already generated tables.

print("All remaining sample data generated in the 'sample_data' directory.")