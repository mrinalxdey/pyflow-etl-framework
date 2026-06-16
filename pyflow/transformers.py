import pandas as pd

def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    # Downcast integers
    for col in df.select_dtypes(include=["int"]):
        df[col] = pd.to_numeric(df[col], downcast="integer")

    # Downcast floats
    for col in df.select_dtypes(include=["float"]):
        df[col] = pd.to_numeric(df[col], downcast="float")

    # Convert low-cardinality object columns to category
    for col in df.select_dtypes(include=["object"]):
        if len(df) > 0:
            unique_ratio = df[col].nunique(dropna=False) / len(df)

            if unique_ratio < 0.05:
                df[col] = df[col].astype("category")

    return df

def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    # Numeric columns
    for col in df.select_dtypes(include=["number"]):
        if df[col].isna().any():
            # Use median if data is skewed
            if abs(df[col].skew()) > 1:
                fill_value = df[col].median()
            else:
                fill_value = df[col].mean()

            df[col] = df[col].fillna(fill_value)

    # Categorical columns
    for col in df.select_dtypes(include=["object", "category"]):
        
        if df[col].isna().any():

            unique_ratio = df[col].nunique(dropna=False) / len(df)

            if unique_ratio < 0.05:
                if not df[col].mode().empty:
                    fill_value = df[col].mode()[0]
                else:
                    fill_value = "Unknown"

                df[col] = df[col].fillna(fill_value)
    
    # Timeseries columns
    for col in df.select_dtypes(include=["datetime"]):
        df[col] = df[col].ffill()
    
    return df