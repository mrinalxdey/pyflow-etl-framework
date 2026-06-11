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

# Average taxi fare by hour of day
