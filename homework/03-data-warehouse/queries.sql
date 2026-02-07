-- 1
SELECT
  COUNT(*)
FROM
  `dezoomcamp_hw3_2025.yellow_tripdata_2024`;

-- 2
SELECT
  COUNT(DISTINCT PULocationID)
FROM
  `dezoomcamp_hw3_2025.yellow_tripdata_2024_external`;

-- 3
SELECT
  PULocationID,
  DOLocationID,
FROM
  `dezoomcamp_hw3_2025.yellow_tripdata_2024`;

-- 4
SELECT
  COUNT(*)
FROM
  `dezoomcamp_hw3_2025.yellow_tripdata_2024`
WHERE
  fare_amount = 0;

-- 5
CREATE TABLE `dezoomcamp_hw3_2025.yellow_tripdata_2024_optimized``
  PARTITION BY TIMESTAMP_TRUNC(tpep_dropoff_datetime, DAY)
  CLUSTER BY VendorID
AS (
  SELECT * FROM `dezoomcamp_hw3_2025.yellow_tripdata_2024`
);

-- 6
SELECT
  COUNT(DISTINCT VendorID)
FROM
  `dezoomcamp_hw3_2025.yellow_tripdata_2024_optimized`
WHERE
  tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
