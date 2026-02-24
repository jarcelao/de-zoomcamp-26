/* @bruin

name: reports.trips_report
type: duckdb.sql
depends:
  - staging.trips
materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
  time_granularity: timestamp
columns:
  - name: pickup_date
    type: date
    description: Pickup date
    primary_key: true
  - name: taxi_type
    type: string
    description: Taxi type (yellow or green)
    primary_key: true
  - name: payment_type_name
    type: string
    description: Payment type name
    primary_key: true
  - name: trip_count
    type: bigint
    description: Number of trips
    checks:
      - name: non_negative
  - name: total_fare
    type: float
    description: Total fare amount
    checks:
      - name: non_negative
  - name: avg_fare
    type: float
    description: Average fare amount
    checks:
      - name: non_negative
  - name: total_trip_distance
    type: float
    description: Total trip distance
    checks:
      - name: non_negative
  - name: avg_trip_distance
    type: float
    description: Average trip distance
    checks:
      - name: non_negative
  - name: total_tip_amount
    type: float
    description: Total tip amount
    checks:
      - name: non_negative

@bruin */

SELECT 
    DATE(pickup_datetime) AS pickup_date,
    taxi_type,
    COALESCE(payment_type_name, 'Unknown') AS payment_type_name,
    COUNT(*) AS trip_count,
    SUM(fare_amount) AS total_fare,
    AVG(fare_amount) AS avg_fare,
    SUM(trip_distance) AS total_trip_distance,
    AVG(trip_distance) AS avg_trip_distance,
    SUM(tip_amount) AS total_tip_amount
FROM staging.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
GROUP BY 
    DATE(pickup_datetime),
    taxi_type,
    COALESCE(payment_type_name, 'Unknown')
