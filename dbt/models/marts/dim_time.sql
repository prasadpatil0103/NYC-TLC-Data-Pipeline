SELECT DISTINCT
    DATE(pickup_datetime)                   AS trip_date,
    MIN(pickup_hour) OVER (
        PARTITION BY DATE(pickup_datetime)
    )                                       AS hour_of_day,
    DAYOFWEEK(DATE(pickup_datetime))        AS day_of_week,
    CASE DAYOFWEEK(DATE(pickup_datetime))
        WHEN 1 THEN 'Sunday'
        WHEN 2 THEN 'Monday'
        WHEN 3 THEN 'Tuesday'
        WHEN 4 THEN 'Wednesday'
        WHEN 5 THEN 'Thursday'
        WHEN 6 THEN 'Friday'
        WHEN 7 THEN 'Saturday'
    END                                     AS day_name,
    MONTH(DATE(pickup_datetime))            AS month,
    YEAR(DATE(pickup_datetime))             AS year,
    CASE WHEN DAYOFWEEK(DATE(pickup_datetime))
        IN (1, 7) THEN TRUE ELSE FALSE
    END                                     AS is_weekend
FROM {{ ref('stg_trips') }}
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY DATE(pickup_datetime)
    ORDER BY pickup_datetime
) = 1