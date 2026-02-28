-- #1
SELECT MIN(trip_pickup_date_time) as earliest_date, 
       MAX(trip_pickup_date_time) as latest_date 
FROM taxi_data_20260228045945.taxi_data;

-- #2
SELECT ROUND(100.0 * COUNT(CASE WHEN LOWER(payment_type) = 'credit' THEN 1 END) / COUNT(*), 2) as credit_pct 
FROM taxi_data_20260228045945.taxi_data;

-- #3
SELECT SUM(tip_amt) as total_tips 
FROM taxi_data_20260228045945.taxi_data;
