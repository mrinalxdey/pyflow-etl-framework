import pandas as pd
from collections import Counter, defaultdict

# Top 10 most frequent pickup locations
trip = pd.read_csv("Data/yellow_tripdata_2024-01.csv")
zone = pd.read_csv("Data/taxi_zone_lookup.csv")

top_10 = Counter(trip['PULocationID']).most_common(10)

top_10_df = pd.DataFrame(
    top_10,
    columns=['LocationID', 'TripCount']
)

result = top_10_df.merge(
    zone,
    on='LocationID',
    how='left'
)

print(result[["LocationID", "Zone", "Borough", "TripCount"]])

def aggregate_trip_metrics(df: pd.DataFrame) -> pd.DataFrame:
    df['date'] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.date
    df['hour'] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.hour

    return (
        df.groupby(['date', 'hour', 'Borough'], as_index=False)
        .agg(
            total_trips=('Borough', 'size'),
            avg_fare=('fare_amount', 'mean'),
            median_fare=('fare_amount', 'median'),
            total_revenue=('fare_amount', 'sum'),
            avg_distance=('trip_distance', 'mean')
        )
    )

def add_borough(trips_df: pd.DataFrame, zones_df: pd.DataFrame) -> pd.DataFrame:
    return trips_df.merge(
        zones_df[["LocationID", "Borough"]],
        left_on="PULocationID",
        right_on="LocationID",
        how='left',
        validate='many_to_one'
    )

merged_df = add_borough(trip, zone)
agg_trip = aggregate_trip_metrics(merged_df)
print(agg_trip)