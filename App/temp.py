keys = "trip_id,taxi_id,trip_start_timestamp,trip_end_timestamp,trip_seconds,trip_miles,dropoff_census_tract,dropoff_community_area,fare,tips,tolls,extras,trip_total,payment_type,company,dropoff_centroid_latitude,dropoff_centroid_longitude,dropoff_centroid_location,pickup_census_tract,pickup_community_area,pickup_centroid_latitude,pickup_centroid_longitude,pickup_centroid_location"
keys = keys.split(',')

for i in range(len(keys)):
    print(f'{i}>{keys[i]}')