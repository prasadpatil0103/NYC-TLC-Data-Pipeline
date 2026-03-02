WITH stg AS (
    SELECT * FROM {{ ref('stg_trips') }}
)

SELECT
    *,
    CASE payment_type
        WHEN 1 THEN 'Credit Card'
        WHEN 2 THEN 'Cash'
        WHEN 3 THEN 'No Charge'
        WHEN 4 THEN 'Dispute'
        ELSE 'Unknown'
    END                             AS payment_type_label,

    CASE
        WHEN trip_distance < 1  THEN 'Short'
        WHEN trip_distance < 5  THEN 'Medium'
        WHEN trip_distance < 15 THEN 'Long'
        ELSE 'Very Long'
    END                             AS trip_category,

    CASE
        WHEN pickup_hour BETWEEN 7  AND 9  THEN 'Morning Rush'
        WHEN pickup_hour BETWEEN 16 AND 19 THEN 'Evening Rush'
        WHEN pickup_hour BETWEEN 0  AND 5  THEN 'Late Night'
        WHEN pickup_hour BETWEEN 22 AND 23 THEN 'Late Night'
        ELSE 'Off Peak'
    END                             AS time_of_day
FROM stg
