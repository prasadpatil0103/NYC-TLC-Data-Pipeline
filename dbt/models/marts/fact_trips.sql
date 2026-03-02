{{ config(
    materialized = 'table'
) }}

WITH enriched AS (
    SELECT * FROM {{ ref('int_trips_enriched') }}
)

SELECT
    {{ dbt_utils.generate_surrogate_key([
        'vendor_id',
        'pickup_datetime',
        'dropoff_datetime',
        'pickup_location_id',
        'dropoff_location_id',
        'total_amount'
    ]) }}                           AS trip_id,
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    pickup_location_id,
    dropoff_location_id,
    payment_type,
    payment_type_label,
    fare_amount,
    tip_amount,
    total_amount,
    trip_duration_min,
    revenue_per_mile,
    tip_percentage,
    trip_category,
    time_of_day,
    pickup_hour,
    pickup_day,
    pickup_month,
    pickup_year,
    is_weekend
FROM enriched
