import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)

# Load reference data
orders = pd.read_csv('sample_data/online_order_aligned.csv')
products = pd.read_csv('sample_data/product.csv')

# Generate online_order_line.csv
num_lines = 2000
online_order_line = pd.DataFrame({
    "OrderLineID": [f"OOL{str(i).zfill(7)}" for i in range(1, num_lines + 1)],
    "OrderID": np.random.choice(orders["OnlineOrderID"], num_lines),
    "ProductID": np.random.choice(products["ProductID"], num_lines),
    "Quantity": np.random.randint(1, 5, num_lines),
    "UnitPrice": np.random.choice(products["UnitPrice"], num_lines)
})
online_order_line.to_csv('sample_data/online_order_line.csv', index=False)
print("Generated online_order_line.csv")