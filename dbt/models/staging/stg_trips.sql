WITH source AS (
    SELECT * FROM {{ source('staging', 'RAW_TRIPS') }}
)

SELECT
    VENDORID                        AS vendor_id,
    PICKUP_DATETIME                 AS pickup_datetime,
    DROPOFF_DATETIME                AS dropoff_datetime,
    COALESCE(PASSENGER_COUNT, 1)    AS passenger_count,
    TRIP_DISTANCE                   AS trip_distance,
    PULOCATIONID                    AS pickup_location_id,
    DOLOCATIONID                    AS dropoff_location_id,
    PAYMENT_TYPE                    AS payment_type,
    FARE_AMOUNT                     AS fare_amount,
    TIP_AMOUNT                      AS tip_amount,
    TOTAL_AMOUNT                    AS total_amount,
    TRIP_DURATION_MIN               AS trip_duration_min,
    REVENUE_PER_MILE                AS revenue_per_mile,
    PICKUP_HOUR                     AS pickup_hour,
    PICKUP_DAY                      AS pickup_day,
    PICKUP_MONTH                    AS pickup_month,
    PICKUP_YEAR                     AS pickup_year,
    IS_WEEKEND                      AS is_weekend,
    TIP_PERCENTAGE                  AS tip_percentage
FROM source
WHERE
    TRIP_DISTANCE > 0
    AND TOTAL_AMOUNT > 0
    AND PICKUP_DATETIME IS NOT NULL
