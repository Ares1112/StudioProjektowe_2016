from kafka import KafkaProducer
from kafka.errors import KafkaError
import time
import sys
import os
import django
from django.utils import timezone
from datetime import timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "TOPR")))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TOPR.settings")
django.setup()

from tourist_app.models import Turysta

turysta = Turysta(numer_telefonu='1234567890', pozycja_N=19.53041, pozycja_E=49.572995, ostatni_ruch=(timezone.now()-timedelta(minutes=14)))
turysta.save()

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

while True:
    producer.send(topic='nadajnik1', key='1234567890', value=b'19.53041, 49.572995')
    producer.flush()
    time.sleep(10)