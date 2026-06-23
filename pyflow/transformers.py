import pandas as pd
import pdb
from pyflow.utils import TransformationError

def optimize_memory(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # pdb.set_trace()
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
    except Exception as e:
        raise TransformationError(f"Failed to optimize memory: {e}") from e

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

def handle_fare_outliers(df: pd.DataFrame) -> pd.DataFrame:
    if "fare_amount" not in df.columns:
        return df
    
    q1 = df['fare_amount'].quantile(0.25)
    q3 = df['fare_amount'].quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    df = df[
        (df["fare_amount"] >= lower_bound)
        & (df["fare_amount"] <= upper_bound)
    ]

    return df

def remove_duplicate_trips(df: pd.DataFrame) -> pd.DataFrame:
    business_keys = [
        "trip_start_time",
        "pickup_location", 
        "dropoff_location"
    ]

    existing_keys = [
        col for col in business_keys
        if col in df.columns
    ]

    if len(existing_keys) != len(business_keys):
        return df
    
    return df.drop_duplicates(subset=business_keys, keep="first")

def merge_trip_data(trips_df: pd.DataFrame = pd.read_csv("Data/yellow_tripdata_2024-01.csv"), 
                    weather_df: pd.DataFrame = pd.read_csv("Data/weather.csv"), 
                    holidays_df: pd.DataFrame = pd.read_csv("Data/holidays.csv")) -> pd.DataFrame:
    
    merged_df = trips_df.merge(
        weather_df,
        how="left",
        on="date",
        validate="many_to_one"
    )
    merged_df = merged_df.merge(
        holidays_df,
        how="left",
        on="date",
        validate="many_to_one"
    )

    return merged_df

def handle_datetime_features(df: pd.DataFrame) -> pd.DataFrame:

    for col in df.columns:
        try:
            parsed = pd.to_datetime(
                df[col],
                errors="coerce"
            )

            # Skip if most values are not valid dates
            if parsed.notna().mean() < 0.8:
                continue

            df[col] = parsed
            df[f"{col}_hour"] = parsed.dt.hour
            df[f"{col}_day_of_week"] = parsed.dt.day_name()
            df[f"{col}_is_weekend"] = (
                parsed.dt.dayofweek >= 5
            )

        except Exception:
            continue

    return df