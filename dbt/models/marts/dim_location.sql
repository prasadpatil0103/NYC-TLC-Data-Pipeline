SELECT DISTINCT
    pickup_location_id              AS location_id,
    COUNT(*) OVER (
        PARTITION BY pickup_location_id
    )                               AS total_pickups
FROM {{ ref('stg_trips') }}
