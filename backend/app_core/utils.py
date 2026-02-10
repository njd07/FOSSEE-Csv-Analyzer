import pandas as pd

# read csv into dataframe
def parse_csv_file(file_obj):
    df = pd.read_csv(file_obj)
    df.columns = df.columns.str.strip()
    return df

# compute stats from equipment dataframe
def compute_summary(df):
    numeric_cols = ['Flowrate', 'Pressure', 'Temperature']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # averages for each param
    averages = {}
    for col in numeric_cols:
        if col in df.columns:
            avg = df[col].mean()
            averages[col] = round(avg, 2) if pd.notna(avg) else 0.0

    # count by equipment type
    type_dist = {}
    if 'Type' in df.columns:
        type_dist = df['Type'].value_counts().to_dict()

    return {
        'total_count': len(df),
        'averages': averages,
        'type_distribution': type_dist,
    }
