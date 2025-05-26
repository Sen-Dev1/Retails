import os

csv_files_outside_sample_data = [f for f in os.listdir('.') if f.endswith('.csv')]
print("CSV files outside sample_data:")
for f in csv_files_outside_sample_data:
    print(f)