/* @bruin

name: staging.trips
type: duckdb.sql
depends:
  - ingestion.trips
  - ingestion.payment_lookup
materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp
columns:
  - name: pickup_datetime
    type: timestamp
    description: Pickup datetime
    primary_key: true
    nullable: false
    checks:
      - name: not_null
  - name: dropoff_datetime
    type: timestamp
    description: Dropoff datetime
    nullable: false
    checks:
      - name: not_null
  - name: passenger_count
    type: integer
    description: Number of passengers
    checks:
      - name: non_negative
  - name: trip_distance
    type: float
    description: Trip distance in miles
    checks:
      - name: non_negative
  - name: fare_amount
    type: float
    description: Fare amount in USD
    checks:
      - name: non_negative
  - name: total_amount
    type: float
    description: Total amount in USD
    checks:
      - name: non_negative
  - name: taxi_type
    type: string
    description: Taxi type (yellow or green)
    nullable: false
    checks:
      - name: not_null
  - name: payment_type_id
    type: integer
    description: Payment type ID
  - name: payment_type_name
    type: string
    description: Payment type name from lookup

@bruin */

WITH deduplicated AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY tpep_pickup_datetime, tpep_dropoff_datetime, pu_location_id, do_location_id, fare_amount
               ORDER BY extracted_at DESC
           ) AS row_num
    FROM ingestion.trips
    WHERE tpep_pickup_datetime >= '{{ start_datetime }}'
      AND tpep_pickup_datetime < '{{ end_datetime }}'
)
SELECT 
    tpep_pickup_datetime AS pickup_datetime,
    tpep_dropoff_datetime AS dropoff_datetime,
    passenger_count,
    trip_distance,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    taxi_type,
    p.payment_type_id AS payment_type_id,
    p.payment_type_name,
    extracted_at
FROM deduplicated d
LEFT JOIN ingestion.payment_lookup p ON d.payment_type = p.payment_type_id
WHERE d.row_num = 1
  AND tpep_pickup_datetime IS NOT NULL
  AND tpep_dropoff_datetime IS NOT NULL
  AND fare_amount >= 0
  AND total_amount >= 0
