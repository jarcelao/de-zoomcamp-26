-- run this script via duckdb
-- .read queries.sql

CREATE OR REPLACE TABLE
    green_tripdata
AS
    SELECT
        *
    FROM
        'green_tripdata_2025-11.parquet';

CREATE OR REPLACE TABLE
    taxi_zone_lookup
AS
    SELECT
        *
    FROM
        'taxi_zone_lookup.csv';

-- q3
SELECT
    COUNT(1)
FROM
    green_tripdata
WHERE
    lpep_pickup_datetime > '2025-11-01'
AND
    lpep_pickup_datetime < '2025-12-01'
AND
    trip_distance <= 1;

-- q4
SELECT
    CAST(lpep_pickup_datetime AS DATE),
    SUM(trip_distance)
FROM
    green_tripdata
WHERE
    trip_distance <= 100
GROUP BY
    CAST(lpep_pickup_datetime AS DATE)
ORDER BY
    SUM(trip_distance) DESC
LIMIT 1;

-- q5
SELECT
    t.Zone,
    SUM(g.total_amount)
FROM
    green_tripdata g
JOIN
    taxi_zone_lookup t
ON
    g.PULocationID == t.LocationID
WHERE
    CAST(lpep_pickup_datetime AS DATE) == '2025-11-18'
GROUP BY
    t.Zone
ORDER BY
    SUM(g.total_amount) DESC
LIMIT
    1;

-- q6
SELECT
    du.Zone,
    MAX(g.tip_amount)
FROM
    green_tripdata AS g
JOIN
    taxi_zone_lookup AS pu
ON
    g.PULocationID = pu.LocationID
JOIN
    taxi_zone_lookup AS du
ON
    g.DOLocationID = du.LocationID
WHERE
    EXTRACT(YEAR FROM g.lpep_pickup_datetime) = 2025
    AND EXTRACT(MONTH FROM g.lpep_pickup_datetime) = 11
    AND pu.Zone = 'East Harlem North'
GROUP BY
    du.Zone
ORDER BY
    MAX(g.tip_amount) DESC
LIMIT
    1;
