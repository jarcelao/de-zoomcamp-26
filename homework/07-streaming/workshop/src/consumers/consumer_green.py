import signal
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from kafka import KafkaConsumer
from models_green import ride_deserializer

server = 'localhost:9092'
topic_name = 'green-trips'

consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=[server],
    auto_offset_reset='earliest',
    group_id='rides-console',
    value_deserializer=ride_deserializer,
    consumer_timeout_ms=10000)

count = 0
count_over_5 = 0

def signal_handler(signum, frame):
    print("\nShutting down...")
    print(f"\nTotal messages received: {count}")
    print(f"Trips with trip_distance > 5: {count_over_5}")
    consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

print(f"Listening to {topic_name}...")

try:
    for message in consumer:
        ride = message.value
        print(f"Received: PU={ride.PULocationID}, DO={ride.DOLocationID}, "
              f"distance={ride.trip_distance}, amount=${ride.total_amount:.2f}")
        count += 1
        if ride.trip_distance > 5:
            count_over_5 += 1
except StopIteration:
    print("\nNo new messages received in 10 seconds, exiting...")
finally:
    print(f"\nTotal messages received: {count}")
    print(f"Trips with trip_distance > 5: {count_over_5}")
    consumer.close()
