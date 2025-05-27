import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# Load reference data
channels = pd.read_csv('sample_data/advertising_channel.csv')
customers = pd.read_csv('sample_data/customer.csv')

# Generate marketing_campaign.csv
num_campaigns = 100
marketing_campaign = pd.DataFrame({
    "CampaignID": [f"MC{str(i).zfill(5)}" for i in range(1, num_campaigns + 1)],
    "ChannelID": np.random.choice(channels["ChannelID"], num_campaigns),
    "StartDate": [fake.date_between(start_date='-2y', end_date='-1y') for _ in range(num_campaigns)],
    "EndDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_campaigns)],
    "Budget": np.random.uniform(1000, 10000, num_campaigns).round(2)
})
marketing_campaign.to_csv('sample_data/marketing_campaign.csv', index=False)
print("Generated marketing_campaign.csv")

# Generate loyalty_points_transaction.csv
num_transactions = 500
loyalty_points_transaction = pd.DataFrame({
    "PointsTransactionID": [f"LPT{str(i).zfill(6)}" for i in range(1, num_transactions + 1)],
    "CustomerID": np.random.choice(customers["CustomerID"], num_transactions),
    "LoyaltyProgramID": [f"LP{str(i).zfill(4)}" for i in np.random.randint(1, 21, num_transactions)],
    "Points": np.random.randint(1, 100, num_transactions),
    "TransactionDate": [fake.date_between(start_date='-1y', end_date='today') for _ in range(num_transactions)]
})
loyalty_points_transaction.to_csv('sample_data/loyalty_points_transaction.csv', index=False)
print("Generated loyalty_points_transaction.csv")