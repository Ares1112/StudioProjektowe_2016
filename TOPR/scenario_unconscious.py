from kafka import KafkaProducer
from kafka.errors import KafkaError
import time

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

while True:
    producer.send(topic='nadajnik1', key='666333111', value=b'19.530410, 49.572995')
    producer.flush()
    time.sleep(10)