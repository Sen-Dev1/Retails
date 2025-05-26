import os
import pandas as pd
from collections import defaultdict

# Directory containing your CSV files
DATA_DIR = '.'

# Get all CSV files in the directory
csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]

# Read columns and data from each CSV file
file_columns = {}
file_data = {}

for file in csv_files:
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, file), dtype=str)  # Read as string for comparison
        file_columns[file] = set(df.columns)
        file_data[file] = df
    except Exception as e:
        print(f"Could not read {file}: {e}")

# Find relationships (shared data) between files
relationships = defaultdict(list)
output_lines = []

for i, file1 in enumerate(csv_files):
    df1 = file_data[file1]
    for j in range(i + 1, len(csv_files)):
        file2 = csv_files[j]
        df2 = file_data[file2]
        shared_columns = []
        for col1 in df1.columns:
            for col2 in df2.columns:
                # Compare unique values in both columns for intersection
                vals1 = set(df1[col1].dropna().unique())
                vals2 = set(df2[col2].dropna().unique())
                shared_vals = vals1 & vals2
                if shared_vals:
                    shared_columns.append(f"{file1}:{col1} <==> {file2}:{col2}")
        if shared_columns:
            output_lines.append(f"\nRelationship(s) found between {file1} and {file2}:")
            for rel in shared_columns:
                output_lines.append(f"  {rel}")

# Write results to a .txt file
with open("column_relationships.txt", "w") as f:
    for line in output_lines:
        f.write(line + "\n")

print("Relationship analysis complete. Results saved to column_relationships.txt.")