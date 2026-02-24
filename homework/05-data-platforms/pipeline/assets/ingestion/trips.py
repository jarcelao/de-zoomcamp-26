"""@bruin

name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default
materialization:
  type: table
  strategy: append
columns:
  - name: VendorID
    type: integer
    description: TLC provider ID
  - name: tpep_pickup_datetime
    type: timestamp
    description: Pickup datetime
  - name: tpep_dropoff_datetime
    type: timestamp
    description: Dropoff datetime
  - name: passenger_count
    type: integer
    description: Number of passengers
  - name: trip_distance
    type: float
    description: Trip distance in miles
  - name: RatecodeID
    type: integer
    description: Rate code ID
  - name: store_and_fwd_flag
    type: string
    description: Store and forward flag
  - name: PULocationID
    type: integer
    description: Pickup location ID
  - name: DOLocationID
    type: integer
    description: Dropoff location ID
  - name: payment_type
    type: integer
    description: Payment type ID
  - name: fare_amount
    type: float
    description: Fare amount
  - name: extra
    type: float
    description: Extra charges
  - name: mta_tax
    type: float
    description: MTA tax
  - name: tip_amount
    type: float
    description: Tip amount
  - name: tolls_amount
    type: float
    description: Tolls amount
  - name: improvement_surcharge
    type: float
    description: Improvement surcharge
  - name: total_amount
    type: float
    description: Total amount
  - name: congestion_surcharge
    type: float
    description: Congestion surcharge
  - name: taxi_type
    type: string
    description: Taxi type (yellow or green)
  - name: extracted_at
    type: timestamp
    description: Extraction timestamp

@bruin"""

import os
import json
from datetime import datetime
from dateutil import parser as date_parser

import pandas as pd
import requests
import pyarrow.parquet as pq


def materialize():
    start_date = os.environ.get("BRUIN_START_DATE", "2022-01-01")
    end_date = os.environ.get("BRUIN_END_DATE", "2022-02-01")
    vars_json = os.environ.get("BRUIN_VARS", "{}")
    variables = json.loads(vars_json)

    taxi_types = variables.get("taxi_types", ["yellow"])

    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data/"

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")

    all_data = []
    current_dt = start_dt

    while current_dt < end_dt:
        year = current_dt.year
        month = current_dt.month

        for taxi_type in taxi_types:
            filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
            url = f"{base_url}{filename}"

            try:
                response = requests.get(url, timeout=60)
                if response.status_code == 200:
                    from io import BytesIO

                    parquet_file = BytesIO(response.content)
                    df = pd.read_parquet(parquet_file)
                    df["taxi_type"] = taxi_type
                    df["extracted_at"] = datetime.now()
                    all_data.append(df)
                    print(f"Downloaded {filename}: {len(df)} rows")
                else:
                    print(
                        f"File not found: {filename} (status: {response.status_code})"
                    )
            except Exception as e:
                print(f"Error downloading {filename}: {e}")

        if month == 12:
            current_dt = datetime(year + 1, 1, 1)
        else:
            current_dt = datetime(year, month + 1, 1)

    if all_data:
        final_df = pd.concat(all_data, ignore_index=True)
        return final_df
    else:
        return pd.DataFrame()
