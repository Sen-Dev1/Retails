import os
import pandas as pd

DATA_DIR = "sample_data"

def get_csv_columns(data_dir):
    """Return a dict of {filename: set(columns)} for all CSVs in the directory."""
    columns = {}
    for fname in os.listdir(data_dir):
        if fname.endswith('.csv'):
            try:
                df = pd.read_csv(os.path.join(data_dir, fname), nrows=0)
                columns[fname] = set(df.columns)
            except Exception as e:
                print(f"Could not read {fname}: {e}")
    return columns

def auto_detect_relationships(columns):
    """Auto-detect relationships by matching likely foreign key columns (ending with 'ID') across files."""
    relationships = []
    col_index = {}
    for fname, cols in columns.items():
        for col in cols:
            if col.lower().endswith("id"):
                col_index.setdefault(col, []).append(fname)
    for col, files in col_index.items():
        if len(files) > 1:
            for i in range(len(files)):
                for j in range(len(files)):
                    if i != j:
                        relationships.append((files[i], col, files[j], col))
    relationships = list(set(relationships))
    return relationships
    # Remove duplicates
    
    relationships = list(set(relationships))
    return relationships

def validate_fk(child_file, child_col, parent_file, parent_col):
    child_path = os.path.join(DATA_DIR, child_file)
    parent_path = os.path.join(DATA_DIR, parent_file)
    if not os.path.exists(child_path) or not os.path.exists(parent_path):
        print(f"Skipping {child_file} or {parent_file}: file not found.")
        return
    try:
        child_df = pd.read_csv(child_path, usecols=[child_col])
        parent_df = pd.read_csv(parent_path, usecols=[parent_col])
    except Exception as e:
        print(f"Error reading {child_file} or {parent_file}: {e}")
        return
    missing = ~child_df[child_col].isin(parent_df[parent_col])
    if missing.any():
        print(f"[FAIL] {child_file}.{child_col} has {missing.sum()} values not found in {parent_file}.{parent_col}")
    else:
        print(f"[OK] {child_file}.{child_col} is valid against {parent_file}.{parent_col}")

if __name__ == "__main__":
    print("Auto-detecting relationships and validating referential integrity across sample_data...")
    columns = get_csv_columns(DATA_DIR)
    relationships = auto_detect_relationships(columns)
    checked = set()
    for rel in relationships:
        # Avoid checking both (A,B,C,D) and (C,D,A,B)
        rel_key = tuple(sorted([(rel[0], rel[1]), (rel[2], rel[3])]))
        if rel_key in checked:
            continue
        checked.add(rel_key)
        validate_fk(*rel)
    print("Validation complete.")