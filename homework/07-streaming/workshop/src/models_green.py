import json
from dataclasses import dataclass
import pandas as pd


@dataclass
class Ride:
    lpep_pickup_datetime: str
    lpep_dropoff_datetime: str
    PULocationID: int
    DOLocationID: int
    passenger_count: int
    trip_distance: float
    tip_amount: float
    total_amount: float


def _get_val(row, key, default):
    """Helper to get value from row, handling both None and NaN."""
    val = row[key]
    if pd.isna(val):
        return default
    return val


def ride_from_row(row):
    return Ride(
        lpep_pickup_datetime=str(_get_val(row, 'lpep_pickup_datetime', "")),
        lpep_dropoff_datetime=str(_get_val(row, 'lpep_dropoff_datetime', "")),
        PULocationID=int(_get_val(row, 'PULocationID', 0)),
        DOLocationID=int(_get_val(row, 'DOLocationID', 0)),
        passenger_count=int(_get_val(row, 'passenger_count', 0)),
        trip_distance=float(_get_val(row, 'trip_distance', 0.0)),
        tip_amount=float(_get_val(row, 'tip_amount', 0.0)),
        total_amount=float(_get_val(row, 'total_amount', 0.0))
    )


def ride_deserializer(data):
    json_str = data.decode('utf-8')
    ride_dict = json.loads(json_str)
    return Ride(**ride_dict)
