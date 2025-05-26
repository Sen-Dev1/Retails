import os
import pandas as pd

def get_column_data(filepath):
    df = pd.read_csv(filepath, dtype=str)  # Read all as string for comparison
    col_data = {}
    for col in df.columns:
        # Use set of non-null, stripped values for comparison
        col_data[col] = set(df[col].dropna().astype(str).str.strip())
    return col_data

def find_matching_columns(csv_files):
    file_columns = {}
    for file in csv_files:
        file_columns[file] = get_column_data(file)

    matches = []
    files = list(file_columns.keys())
    for i in range(len(files)):
        for j in range(i+1, len(files)):
            file1, file2 = files[i], files[j]
            cols1, cols2 = file_columns[file1], file_columns[file2]
            for col1, data1 in cols1.items():
                for col2, data2 in cols2.items():
                    if data1 == data2 and data1:  # Non-empty and exact match
                        matches.append((file1, col1, file2, col2))
    return matches

if __name__ == "__main__":
    # Change '.' to your CSV directory if needed
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    matches = find_matching_columns(csv_files)
    with open("readme1", "w") as f:
        if matches:
            f.write("Matching columns found:\n")
            for file1, col1, file2, col2 in matches:
                f.write(f"{file1}:{col1} <==> {file2}:{col2}\n")
        else:
            f.write("No matching columns found.\n")