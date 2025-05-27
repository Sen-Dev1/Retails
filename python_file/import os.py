import os
import pandas as pd

def get_csv_columns(folder='.'):
    columns = {}
    for filename in os.listdir(folder):
        if filename.endswith('.csv'):
            try:
                df = pd.read_csv(os.path.join(folder, filename), nrows=0)
                columns[filename] = list(df.columns)
            except Exception as e:
                print(f"Could not read {filename}: {e}")
    return columns

def check_column_data_subset(folder, file1, col1, file2, col2):
    try:
        df1 = pd.read_csv(os.path.join(folder, file1), usecols=[col1])
        df2 = pd.read_csv(os.path.join(folder, file2), usecols=[col2])
        set1 = set(df1[col1].dropna().unique())
        set2 = set(df2[col2].dropna().unique())
        if set1 and set1.issubset(set2):
            return True
    except Exception as e:
        print(f"Could not compare {file1}:{col1} and {file2}:{col2}: {e}")
    return False

def find_data_relationships(folder='.'):
    columns_dict = get_csv_columns(folder)
    files = list(columns_dict.keys())
    relationships = []
    for i, file1 in enumerate(files):
        for file2 in files:
            if file1 == file2:
                continue
            for col1 in columns_dict[file1]:
                for col2 in columns_dict[file2]:
                    if check_column_data_subset(folder, file1, col1, file2, col2):
                        relationships.append((file1, col1, file2, col2))
    return relationships

def main():
    folder = '.'
    relationships = find_data_relationships(folder)
    if relationships:
        print("Columns with matching data (subset relationship):")
        for file1, col1, file2, col2 in relationships:
            print(f"{file1}:{col1} ⊆ {file2}:{col2}")
    else:
        print("No data-based relationships found.")

if __name__ == "__main__":
    main()